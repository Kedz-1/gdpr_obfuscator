




# @pytest.mark.parametrize(
#     "csv_multiple_examples, expected_output", [
#         (
#             'name,email\njohn Doe,john.doe@example.com\n',

#             'name,email\n***, ***\n'
        
#         ),
#         (
#             'name,email\njane Doe,jane.doe@example.com\n',

#             'name,email\n***, ***\n'

#         ),
#         (
#             'name,email,age\nalbert Alphonso,albert.alphonso@example.com,35\n',

#             'name,email\n***, ***,35\n'

#         ),
#         (
#             'student_id,name,course,graduation_date,email_address\n1111,john Smith, Software,2024-03-31,j.smith@email.com\n',

#             'student_id,name,course,graduation_date,email_address\n1111,***,Software,2024-03-31,***\n'

#         )
#     ]
# )

# @mock_aws
# def test_csv_files_is_obfuscated(conn, csv_multiple_examples, expected_output):

#     conn.create_bucket(Bucket="test-bucket", CreateBucketConfiguration={"LocationConstraint": "eu-west-2"})

#     conn.put_object(Bucket="test-bucket", Key="test-object", Body=csv_multiple_examples)

#     input1 = conn.get_object(Bucket="test-bucket", Key="test-object")["Body"].read().decode()

    
#     result = obfuscation_tool(input1)

#     assert result == expected_output
