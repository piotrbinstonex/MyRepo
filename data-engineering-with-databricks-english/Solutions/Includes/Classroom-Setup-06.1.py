# Databricks notebook source
# MAGIC %run ./_utility-methods

# COMMAND ----------

class DataFactory:
    def __init__(self, ):
        self.source = f"{DA.paths.datasets}/healthcare/tracker/streaming"
        self.userdir = f"{DA.paths.working_dir}/tracker"
        self.curr_mo = 1
    
    def load(self, continuous=False):
        if self.curr_mo > 12:
            print("Data source exhausted\n")
            
        elif continuous == True:
            while self.curr_mo <= 12:
                curr_file = f"{self.curr_mo:02}.json"
                dbutils.fs.cp(self.source + curr_file, self.userdir + curr_file)
                self.curr_mo += 1
        else:
            curr_file = f"{str(self.curr_mo).zfill(2)}.json"
            target_dir = f"{self.userdir}/{curr_file}"
            print(f"Loading the file {curr_file} to the tracker dataset")
            dbutils.fs.cp(f"{self.source}/{curr_file}", target_dir)
            self.curr_mo += 1

# COMMAND ----------

DA = DBAcademyHelper(**helper_arguments)
DA.reset_environment()
DA.init(install_datasets=True, create_db=True)

DA.data_factory = DataFactory()
print()

DA.data_factory.load()
DA.conclude_setup()

sqlContext.setConf("spark.sql.shuffle.partitions", spark.sparkContext.defaultParallelism)
