TODO:

figure out how to make artifacts of the game
figure out how to use remote workers

figure out how to mock s3 and kicking off pipelines
  fixture file -> s3 <- ??? -> prefect pipeline -> rds/whatever
  goal is to be able to add new files, do the schema detection/translation/whatever, then push to an output schema
  