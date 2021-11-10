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

---
from unintest.mock import patch
with patch('sys.stdout', new=StringIO()) as fake_out:
	print("hello")
	std_output: str = fake_out.getvalue()
	self.assertTrue(std_output=="hello")


---
  @patch('sys.stdout', new_callable=StringIO)
   def test(self,mock_stdout):
      hello()
      output = mock_stdout.getvalue()
      assert "Hello World" in output


---
# where log is member of data_api_proxy

    @unittest.mock.patch('wondersign_list_comparator.data_api.data_api_proxy.log')
    def test_reading_data_from_unstable_api(self, mock_log):
        self.assertTrue(">> next reading attempt from DataApi " in mock_log.method_calls[0].args[0])
        self.assertTrue(">> next reading attempt from DataApi " in mock_log.method_calls[1].args[0])
        self.assertTrue(">> cancel reading from DataApi " in mock_log.method_calls[2].args[0])
	

