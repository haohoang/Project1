# Project1
processXMLFile.py dùng để lấy file text từ file.xml và loại bỏ các kí tự hhtp, dấu ngoặc đơn,... chỉ dữ lại các dấu câu như
".", "!", "?". Kết quả sẽ là 1 file text.

clean_save_file.py dùng để loại bỏ stop word, đưa các từ về dạng nguyên bản, tách câu và tách từ. Sau đó lưu mỗi dòng
một câu vào file.

train_model.py dùng để đưa các câu đã lưu trong file ở trên vào model word2vec. Sau khi đã học từ lưu model vào file.

test.py kiểm tra độ chính xác của model vừa học được.
