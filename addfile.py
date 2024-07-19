for file in pdf_files:
  conn = duckdb.connect(DATABASE_PATH)
  conn.execute("""
  INSERT INTO pdf_files 
  VALUES (nextval('seq_fileid'),'{file_path}', '{file_name}')
  ON CONFLICT (id) DO NOTHING;
  """.format(file_path = os.path.join(path,file), file_name = file))
  conn.close()
