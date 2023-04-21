import tensorflow as tf


class ProductModel(tf.keras.Model):

    def __init__(self,
                 unique_product_names,
                 products):
        super().__init__()

        self.embedding_dimension = 32
        max_tokens = 10_000

        # Title embedding
        self.title_embedding = tf.keras.Sequential([
            tf.keras.layers.StringLookup(vocabulary=unique_product_names, mask_token=None),
            tf.keras.layers.Embedding(len(unique_product_names) + 1, 32)
        ])

        # Title vectorizer
        self.title_vectorizer = tf.keras.layers.TextVectorization(
            max_tokens=max_tokens)

        # Title text embedding
        self.title_text_embedding = tf.keras.Sequential([
            self.title_vectorizer,
            tf.keras.layers.Embedding(max_tokens, 32, mask_zero=True),
            tf.keras.layers.GlobalAveragePooling1D(),
        ])

        # Adapt the title vectorizer to the data.
        self.title_vectorizer.adapt(products)

    def call(self, titles, **kwargs):
        return tf.concat([
            self.title_embedding(titles),
            self.title_text_embedding(titles),
        ], axis=1)
