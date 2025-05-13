This is a website built by Keegan Li, Justin Clarke, and Ainsli Shah using HTML, CSS, and JavaScript.

File Structure:
Minecraft-Crafting-Recipes repo
|
|- data/
|  |- Crafting_Table_Top.png - image of a crafting table top grid used as the background for the crafting section of the quiz
|  |- Crafting_Table.png - crafting table icon used on the left side of the navbar
|  |- Minecraft_Background.jpg - image of minecraft landscape used as the website background
|  |- scores.json - json file to track quiz attempts/scores
|
|- templates/
|  |- base.html - base template for all pages
|  |- category.html - template for /category pages (/basics, /tools, and /defense) that display all items in each category
|  |- crafting.html - template for /quiz/craft pages where the user crafts items as part of the quiz
|  |- index.html - home page
|  |- learn.html - template for /learn pages that show the info for a specific item
|  |- quiz_results.html - page that displays the quiz results
|  |- quiz.html - quiz page that prompts the user with questions
|  |- wrong_answer.html - not used in the program!
|
|- README.txt - this file
|
|- server.py - flask backend server code

To run the project locally, clone the repository, install Flask if necessary, run python server.py.
The terminal will give a link to go to in the browser (Ex: http://127.0.0.1.5001) which should navigate to the home page.
To reset the cache and website progress use /reset_session.