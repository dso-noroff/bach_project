from recommender_user_model import UserModel
import tensorflow as tf


class QueryModel(tf.keras.Model):
    """Model for encoding user queries."""

    def __init__(self,
                 layer_sizes,
                 unique_user_ids,
                 timestamp_buckets,
                 timestamps,
                 unique_colors,
                 products,
                 unique_category_names):
        """Model for encoding user queries.

        Args:
          layer_sizes:
            A list of integers where the i-th entry represents the number of units
            the i-th layer contains.
        """
        super().__init__()

        # Define the UserModel.
        self.embedding_model = UserModel(unique_user_ids,
                                         timestamp_buckets,
                                         timestamps,
                                         unique_colors,
                                         products,
                                         unique_category_names)

        # Then construct the layers.
        self.dense_layers = tf.keras.Sequential()

        # Use the ReLU activation for all but the last layer.
        for layer_size in layer_sizes[:-1]:
            self.dense_layers.add(tf.keras.layers.Dense(layer_size, activation="relu"))

        # No activation for the last layer.
        for layer_size in layer_sizes[-1:]:
            self.dense_layers.add(tf.keras.layers.Dense(layer_size))

    def call(self, inputs, **kwargs):
        feature_embedding = self.embedding_model(inputs)
        return self.dense_layers(feature_embedding)
