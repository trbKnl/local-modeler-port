<p align="center">
  <a href="https://github.com/d3i-infra/feldspar">
    <img width="40%" height="40%" src="./public/port_logo.svg">
  </a>
</p>

# Data donation task for Next

The data donation task is part of a research tool that enables researchers to collected digital trace data for academic research from participants in a secure, transparent, and privacy-preserving way.

Data donation allows researchers to invite participants to share their data download packages (DDPs).
A major challenge is however that DDPs potentially contain very sensitive data, and often not all data is needed to answer the specific research question under investigation.
To circumvent these challenges, the following framework framework was developed:

1. The research participant requests their personal DDP at the platform of interest.
2. They download it onto their own personal device.
3. By means of local processing (i.e. in the browser of the participant) only the features of interest to the researcher are extracted from that DDP.
4. The participant inspects the extracted features after which they can consent (or decline) to donate.

To allow for step 3 and 4 to take place the data donation task is. The data donation task is front end that guides participants through the data donation steps.
The data donation task is primarily created to be used in conjunction with [Next](https://github.com/eyra/mono). 
Next is a software as a service platform developed by [Eyra](https://eyra.co/) to facilitate scientific research.


## How does the data donation task work?

**The idea behind the data donation task**

This data donation task repository contains in essence a toolkit with which you can build your own data donation flow. The donation flow is at the heart of the data donation task, and is at the core of a data donation study. 
It is the step where the participant is actually going to donate their data.

The data donation flow goes as follows:

1. The participant goes to your data donation task app in a browser
2. The participant is prompted to submit their data download package (DDP)
3. A Python script you wrote, extracts the data you need for your research
4. That data gets presented to the participant on screen. (The participant gets to interact with their data)
5. The participants decides to donate and you receive the data 

We opted for a toolkit approach because it offers several benefits:

1. Every study requires unique elements for its participants, and a toolkit can facilitate the creation of this distinct experience.
2. You can extract (and possibly aggregate) only the data you need for your study, which we believe is important in order to preserve the privacy of the participant and is often required by an ethical review board.


**The design of the data donation task**

The data donation task has reusable components (such as: a screen that prompts the participant to submit their DDP and a screen with tables that the participants need to review prior to donation) that you can use and combine/rearrange in creative ways to make your own study.
These components are combined in a Python script that is created by the researcher or a research engineer.

On a high level the script works as follows:

1. The Python script determines which user interface (UI) component needs to be shown to the participant
2. The participant interacts with the UI component on screen. Whenever the participant is done interacting with the UI component, the result of that interaction is returned to the script.
3. The script handles the return result en determine the next UI component that the participant needs to see or interact with, go back to step 1 until the end of the donation flow.


**Creating your own study**

A researcher can implement their own data donation flow by altering a Python script included in this repository called [`script.py`](src/framework/processing/py/port/script.py).
`script.py` has 2 different purposes:

1. It determines the data donation flow. i.e. what screens (for example a file prompt) does the participant gets to see and when. 
2. You can place functions here that extract the data you are interested in from the participants submission. Here is were Python really shines, you can use most data extraction methods you are familiar with! (As long as it's available in [Pyodide](https://pyodide.org/en/stable/))

A typical script includes the following steps:

1. Prompt the participant to submit a file
2. Handling the submission from step 1. This is the step where you can extract the data you are interested in.
3. The extracted data is presented on screen accompanied with a consent button. After consent is given, the data is sent to a storage location of the researcher (not included in the data donation task).

A example such a script is included in this repo: [`script.py`](src/framework/processing/py/port/script.py).
We recommend you use that script as starting point for your own data donation study.

Check out the [documentation](https://d3i-infra.github.io/data-donation-task/) for a tutorial on how to start writing your own `script.py`.


## Installation of the data donation task

In order to start a local instance of the data donation task go through the following steps:

0. Pre-requisites

   - Fork or clone this repo
   - Install [Node.js](https://nodejs.org/en)
   - Install [Python](https://www.python.org/)
   - Install [Poetry](https://python-poetry.org/)

1. Install dependencies & tools:

   ```sh
   npm install
   ```

2. Start the local web server:

   ```sh
   npm run start
   ```

3. You can now go to the browser: [`http://localhost:3000`](http://localhost:3000).

If the installation went correctly you should be greeted with a mock data donation study. 
For detailed installation instructions see the [documentation](https://d3i-infra.github.io/data-donation-task/).


## Feldspar and Next

The data donation task is primarily created to be used in conjunction with [Next](https://github.com/eyra/mono). Next is a software as a service platform developed by [Eyra](https://eyra.co/) to facilitate scientific research.
The data donation task is a fork of [Feldspar](https://github.com/eyra/feldspar) with some extra functionalities added to it. Feldspar is a framework which can be used to build applications specifically for Next. An example of such an application is the data donation task which you can find in this repository. 

For detailed information on how to deploy the data donation task with Next check the [documentation](https://d3i-infra.github.io/data-donation-task/).

_Note_: The data donation task is only a *front end* to be used with Next. In order for it to be used in a live study it needs to be hosted with Next.
The wiki will discuss the options you have for using the data donation task in an actual study.


## Documentation

Here you can find the [documentation](https://d3i-infra.github.io/data-donation-task/)


## Contributing

We want to make contributing to this project as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features

If you have any questions, find any bugs, or have any ideas, read how to contribute [here](https://github.com/eyra/port/blob/master/CONTRIBUTING.md).

## Citation

If you use this repository in your research, please cite it as follows:

```
@article{Boeschoten2023,
  doi = {10.21105/joss.05596},
  url = {https://doi.org/10.21105/joss.05596},
  year = {2023},
  publisher = {The Open Journal},
  volume = {8},
  number = {90},
  pages = {5596},
  author = {Laura Boeschoten and Niek C. de Schipper and Adriënne M. Mendrik and Emiel van der Veen and Bella Struminskaya and Heleen Janssen and Theo Araujo},
  title = {Port: A software tool for digital data donation},
  journal = {Journal of Open Source Software}
}
```

You can find the full citation details in the [`CITATION.cff`](CITATION.cff) file.
