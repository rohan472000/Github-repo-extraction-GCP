# Github-repo-extraction-GCP
Extracted the top 100 repo with highest stars and keeps into BigQuery, extracted different attributes like number of stars,name of repo, language used, date of creation and visualized through Looker.


Visulization: Language used in repo, JS is used in most repos.
![Screenshot (93)](https://user-images.githubusercontent.com/96521078/224222318-ff8ea175-b60e-436f-aeb1-420c7b1bcbb9.png)

2nd color has no name because in many repos the data fetched for language used is empty/null.
We can update that null by any name using below command :-

      UPDATE `project.dataset.table`
      SET language = 'xyz'
      WHERE language IS NULL
  
  -- in above code, `language` is a column name.
  
  
  
You can follow below link for the Blog which will give more explanation of this project.

https://rohan-anand.hashnode.dev/github-the-place-where-we-fork
