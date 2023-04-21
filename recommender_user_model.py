import tensorflow as tf


class UserModel(tf.keras.Model):

    def __init__(self,
                 unique_user_ids,
                 timestamp_buckets,
                 timestamps,
                 unique_colors,
                 products,
                 unique_category_names):
        super().__init__()

        self.embedding_dimension = 32
        max_tokens = 10_000

        # User embedding
        self.user_embedding = tf.keras.Sequential([
            tf.keras.layers.IntegerLookup(vocabulary=unique_user_ids, mask_token=None),
            tf.keras.layers.Embedding(len(unique_user_ids) + 1, 32),
        ])

        # Timestamp embedding
        self.timestamp_embedding = tf.keras.Sequential([
            tf.keras.layers.Discretization(timestamp_buckets.tolist()),
            tf.keras.layers.Embedding(len(timestamp_buckets) + 1, 32),
        ])
        self.normalized_timestamp = tf.keras.layers.Normalization(
            axis=None
        )

        # Adapt the normalization layer to the data.
        self.normalized_timestamp.adapt(timestamps)

        # Color embedding
        self.color_embedding = tf.keras.Sequential([
            tf.keras.layers.experimental.preprocessing.StringLookup(vocabulary=unique_colors, mask_token=None),
            tf.keras.layers.Embedding(len(unique_colors) + 1, self.embedding_dimension)
        ])

        # Color vectorizer
        self.color_vectorizer = tf.keras.layers.experimental.preprocessing.TextVectorization(max_tokens=max_tokens)

        # Color text embedding
        self.color_text_embedding = tf.keras.Sequential([
            self.color_vectorizer,
            tf.keras.layers.Embedding(max_tokens, self.embedding_dimension, mask_zero=True),
            tf.keras.layers.GlobalAveragePooling1D(),
        ])

        # Adapt the color vectorizer to the data.
        self.color_vectorizer.adapt(products)

        # Category embedding
        self.category_embedding = tf.keras.Sequential([
            tf.keras.layers.experimental.preprocessing.StringLookup(vocabulary=unique_category_names, mask_token=None),
            tf.keras.layers.Embedding(len(unique_category_names) + 1, self.embedding_dimension)
        ])

        # Category vectorizer
        self.category_vectorizer = tf.keras.layers.experimental.preprocessing.TextVectorization(max_tokens=max_tokens)

        # Category text embedding
        self.category_text_embedding = tf.keras.Sequential([
            self.category_vectorizer,
            tf.keras.layers.Embedding(max_tokens, self.embedding_dimension, mask_zero=True),
            tf.keras.layers.GlobalAveragePooling1D(),
        ])

        # Adapt the category vectorizer to the data.
        self.category_vectorizer.adapt(products)

    def call(self, inputs, **kwargs):
        # Take the user ID, timestamp, color, and category name, and pass them, along with the
        # normalized timestamp, through the respective embedding layers.
        return tf.concat([
            self.user_embedding(inputs["user_id"]),
            self.timestamp_embedding(inputs["order_time_stamp"]),
            self.color_embedding(inputs["color"]),
            self.color_text_embedding(inputs["color"]),
            self.category_embedding(inputs["category_name"]),
            self.category_text_embedding(inputs["category_name"]),
            tf.reshape(self.normalized_timestamp(inputs["order_time_stamp"]), (-1, 1)),
        ], axis=1)
