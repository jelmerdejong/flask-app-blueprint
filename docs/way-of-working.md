# Make it your own!
That was easy right? You are ready to go modify and built your next killer app. Few points to keep in mind:

1. Don't forget to commit your code and push to Github as backup ($ git push origin master)
2. Run $ flake8 projectname to get feedback on coding style
3. Deploy to staging as final test ($ git push staging master)
4. Finally: deploy to product ($ git push production master)

## Working with pip
When you first start using Flask App Blueprint you install all the required dependencies through pip, by running `pip install -r requirements.txt`. When you install new packages (by running `pip install SomePackage`), make sure to also update the requirements.txt file so next time you run `pip install -r requirements.txt` also the newly installed packages are part of you project. You can do this by running `pip freeze > requirements.txt`.

More on pip: https://pip.pypa.io/en/stable/user_guide/
