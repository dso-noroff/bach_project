from recommender_product_model import ProductModel
import tensorflow as tf


class CandidateModel(tf.keras.Model):
    """Model for encoding products."""

    def __init__(self,
                 layer_sizes,
                 unique_product_names,
                 products):
        """Model for encoding products.

        Args:
          layer_sizes:
            A list of integers where the i-th entry represents the number of units
            the i-th layer contains.
        """
        super().__init__()

        # Define the ProductModel.
        self.embedding_model = ProductModel(unique_product_names, products)

        # Construct the layers.
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
