CREATE TABLE [Tasks] ( 
	[Task_id] INTEGER  NOT NULL PRIMARY KEY, 
	[Task_subject] NVARCHAR(500)  , 
	[Task_description] NVARCHAR(500) , 
	[created_at] date , 
	[created_by] VARCHAR(500) , 
	[assigned_to] VARCHAR(500)  ,
	[is_complete] SMALLINT 
); 
CREATE TABLE [Files] (  
	[file_id] INTEGER  PRIMARY KEY NOT NULL,
	[file_name] NVARCHAR(500) , 
	[task_id] INTEGER ,   
	[data]  BLOB  
);