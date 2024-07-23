# dynamo-buddy

DYNAMO is a small software program with which you can calculate prediction models.
Dynamo-buddy can help you create transition matrices and configurations with multiple scenario's (optionally for multiple age groups), which can be imported in Dynamo. It's an automation of what else is a lot of manual work in Dynamo itself.

## How to use
1. Download and unpack the dynamo-buddy.zip on your computer.
2. Double-click/Run the run.exe file.
3. An application will be opened in the browser, in the sidebar on the left you will find multiple pages you can visit.

![image](https://github.com/user-attachments/assets/9864f760-5cbe-4d7b-9168-32d354795692)
<img width="956" alt="351413088-d54d4ab2-0364-409d-a5ea-263ae2f8df91" src="https://github.com/user-attachments/assets/56ed4536-c2fe-4aec-812d-ff5c802adbaa">

### Use case 1: Transition matrix
On the page 'Transition Matrix' you can create transition matrices by first specifying the number of categories (for example 3 categories like 'non-smoker', 'former smoker', 'current smoker'). Second, you can design multiple transition rules. Per transition rule you select a gender (Male, Female, or both), and an age range (start age and stop age). On the right you see a small table where you can set the transition chances. You can edit this table, change the example numbers in there, add/delete rows, etc. 
After setting your first transition rule, you could continue as is, or use the 'Add' and 'Delete' buttons to create/delete rules. Every new rule will overwrite the previous one if there are overlapping groups selected.
The big table below shows how the transition matrix will look like.
When you are happy with the example matrix you can press the 'Create transitionmatrix' button. A file will be generated which you can see at 'Manage Files', you can find this file on your computer: next to the run.exe file you can find the folder content > output. Everything dynamo-buddy creates for you will be in here.

![image](https://github.com/user-attachments/assets/59a3d457-1944-4162-8ef9-c766f49be5ab)
![image](https://github.com/user-attachments/assets/d54d4ab2-0364-409d-a5ea-263ae2f8df91)


### Use case 2: Create Configurations - Scenario's
When you create a simulation in Dynamo you have to specify a lot of settings before running the model. Dynamo-buddy does not do the WHOLE configuration, so you will have to do this once in Dynamo (only include 1 scenario!), then you can take the configuration.xml file from dynamo and give it to dynamo-buddy. You can give it to your buddy by using the tab 'Manage files'. After that you can use the 'Create Configurations - Scenario's' page to create a configuration file with multiple scenario's for different success rates. The success rates will be varied between 0 and 100 in equal bins depending on the number of scenario's you choose, so choose wisely. When you pressed the 'Create configuration(s)' button there, again, will be a .xml file stored in the output folder. If you import it in Dynamo you will see that this was an easy way to create multiple scenario's, you can still adjust things in Dynamo now. 

![image](https://github.com/user-attachments/assets/0a76da20-de1e-4342-9b73-4fe04eb7b7b5)


### Use case 3: Create Configurations - Age Groups
Same as for use case 2 you will need an input configuration.xml from Dynamo. But after that you can set the number of scenario's, and define age groups. This table is editable, so add as many rows (i.e. age groups) as you like. The 'Create configuration(s)' button will create a configuration file per age group, which can be imported in Dynamo.

![image](https://github.com/user-attachments/assets/69dacc2d-642b-4c3f-a9b0-89b5f3f67ba5)



## Feedback
We hope that dynamo-buddy can help you and reduce some endless manual-clicking for you.
Let us know if you have suggestions, ideas, or feature requests.
