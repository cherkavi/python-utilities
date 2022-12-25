import mlflow
import mlflow.sklearn

mlflow.start_run(experiment_id="my_experiment")

mlflow.log_param("param1", 5)
mlflow.log_param("param2", "value2")

# Train a model
from sklearn.ensemble import RandomForestRegressor
model = RandomForestRegressor()
model.fit(x_train, y_train)

# Log model as artifact
mlflow.sklearn.log_model(model, "random-forest-model")

# Log metrics
mlflow.log_metrics("mse", mean_squared_error(y_test, model.predict(x_test)))
mlflow.log_metrics("mse", mean_absolute_error(y_test, model.predict(x_test)))