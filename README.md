# Project X AE A-12 : FakeNews detector from a Twitter database



## Contributors [Group 1]

- [Sohel Dinoo](https://gitlab-cw4.centralesupelec.fr/sohel.dinnoo)
- [Alexandre Baux](https://gitlab-cw4.centralesupelec.fr/alexandre.baux)
- [Philémon Wehbe](https://gitlab-cw4.centralesupelec.fr/philemon.wehbe)
- [Mathis Rouget](https://gitlab-cw4.centralesupelec.fr/mathis.rouget)
- [Zein Sakkour](https://gitlab-cw4.centralesupelec.fr/zein.sakkour)
- [Vianney Saint Georges-Chaumet](https://gitlab-cw4.centralesupelec.fr/vianney.saintgeorges-chaumet)

## Project context and description

<p style='text-align : justify'> 
    Nowadays, fake news are widely spread on social media et especially on Twitter (X). Furthermore, it is for big companies, politicians and other renowned people important to control their digital and public reputation. Therefore, our product appears as a tool for such clients to keep track and battle misinformation and could be used by unique users but also by private companies. 
    <br>
    <br>
    Our project aims to detect fake news and to rank them. Depending on its impact on other users, how viral it is and other criteria, our program allows the consumer to follow the evolution of a piece of fake news through time. 
</p>

## Needs analysis

**Tweet analysis:** 

<ul style='text-align : justify'> 
    <li> A unique user will be able to access some (limited) information about a chosen subject (free account). </li>
    <li>Companies or more widely known organizations should be able to follow the digital opinion about them (premium account).</li>
    <li> As seen higher, we could monetize our services through a subscription service to access better options (such as Twitter Blue). Free accounts will be able to have access to a limited number of requests using tweets published only recently (a week-widthspan) Premium accounts will be able to have access to unlimited requests over tweets over a longer period. </li>
</ul>

## Machine Learning Implementation
Our machine learning (ML) implementation focuses on predicting fake news labels and estimating probabilities for articles in a given dataset using a trained model. The key steps involve data preprocessing, model training, prediction, and updating the dataset with predictions and probabilities. <br>
The first step is loading the training dataset, which includes labeled examples of fake and real news. The labels are extracted, and the textual content is used as the input feature. We employ a TfidfVectorizer, initialized with specific parameters such as stop words and maximum document frequency, to convert the text into a numerical representation suitable for machine learning.<br>
We utilize a PassiveAggressiveClassifier, a popular algorithm for online learning scenarios. This classifier is trained on the Tfidf-transformed training data to learn the patterns and characteristics of fake and real news.<br>
Once the model is trained, it is used to predict labels and decision function scores on the dataset to be evaluated. The TfidfVectorizer is also applied to transform the text in the dataset into a suitable format for prediction.<br>
The decision function scores obtained from the model are converted into probabilities. These probabilities represent the confidence of the model in assigning the "FAKE" label. The dataset is then updated with the predicted labels and corresponding probabilities.<br>
This ML implementation provides a robust and effective way to classify news articles as fake or real based on the patterns learned during training. The update mechanism ensures that the dataset reflects the model's predictions and enables further analysis and actions based on these predictions.

## Installation instructions
Install all needed packages by running `pip install -r requirements.txt`.

Clone the `git` repository on your computer with `git clone`.

Download the dataset on : <span style = 'background-color : red; color : white'> insert url here </span>.

Move the `.csv` file into the folder `./data`.

Go to <span style = 'background-color : red; color : white'> insert local url here </span>.

## How to use the app ?
Run the app with `python run main.py` in a terminal.

## Code architecture diagram
![Code architecure diagram](./doc/code_architecture.png)

 