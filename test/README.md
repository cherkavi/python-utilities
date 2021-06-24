from testfixtures import LogCapture

  with LogCapture(names=AIRFLOW_TASK_LOGGER, level=logging.INFO) as capture:

	# some actions here 
        capture.check(
            (AIRFLOW_TASK_LOGGER, "INFO", f"Checking if image exists."),
            (AIRFLOW_TASK_LOGGER, "INFO", f"Image found."),
        )


# catch exception 
	with self.assertRaises(ShopifyException) as ex:
            service_variants.add(result_standalone["product"]["id"], product_variant)
        self.assertTrue("{'price': [\"can't be blank\"]}" in ex.exception.message )

