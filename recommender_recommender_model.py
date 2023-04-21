from recommender_query_model import QueryModel
from recommender_candidate_model import CandidateModel

import tensorflow as tf
import tensorflow_recommenders as tfrs


class RecommenderModel(tfrs.models.Model):

    def __init__(self,
                 layer_sizes,
                 rating_weight: float,
                 retrieval_weight: float,
                 unique_product_names,
                 products,
                 unique_user_ids,
                 timestamp_buckets,
                 timestamps,
                 unique_colors,
                 unique_category_names):
        super().__init__()

        # Define the query model.
        self.query_model = QueryModel(layer_sizes,
                                      unique_user_ids,
                                      timestamp_buckets,
                                      timestamps,
                                      unique_colors,
                                      products,
                                      unique_category_names)

        # Define the candidate model.
        self.candidate_model = CandidateModel(layer_sizes,
                                              unique_product_names,
                                              products)

        # Define the rating model.
        self.rating_model = tf.keras.Sequential([
            tf.keras.layers.Dense(256, activation="relu"),
            tf.keras.layers.Dense(128, activation="relu"),
            tf.keras.layers.Dense(1)
        ])

        # Define the rating task.
        self.rating_task = tfrs.tasks.Ranking(
            loss=tf.keras.losses.MeanSquaredError(),
            metrics=[tf.keras.metrics.RootMeanSquaredError()]
        )

        # Define the retrieval task.
        self.retrieval_task = tfrs.tasks.Retrieval(
            metrics=tfrs.metrics.FactorizedTopK(
                candidates=products.batch(128).map(self.candidate_model),
            )
        )

        # Set the weights for the rating and retrieval tasks.
        self.rating_weight = rating_weight
        self.retrieval_weight = retrieval_weight

    def call(self, inputs, **kwargs):
        user_embeddings = self.query_model({"user_id": inputs["user_id"]})
        product_embeddings = self.candidate_model(inputs["product_name"])
        return (user_embeddings, product_embeddings,
                self.rating_model(tf.concat([user_embeddings, product_embeddings], axis=1)))

    def compute_loss(self, features, **kwargs):
        # Extract the order quantities.
        quantities = features.pop("order_quantity")

        # Define the query embeddings.
        query_embeddings = self.query_model({
            "user_id": features["user_id"],
            "order_time_stamp": features["order_time_stamp"],
            "color": features["color"],
            "category_name": features["category_name"]
        })

        # Define the candidate embeddings.
        product_embeddings = self.candidate_model(features["product_name"])

        # Define the rating prediction and loss.
        rating_predictions = self.rating_model(tf.concat([query_embeddings, product_embeddings], axis=1))
        rating_loss = self.rating_task(labels=quantities, predictions=rating_predictions)
        retrieval_loss = self.retrieval_task(query_embeddings, product_embeddings)

        return self.rating_weight * rating_loss + self.retrieval_weight * retrieval_loss
