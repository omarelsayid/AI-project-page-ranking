# PageRank Project

This project implements the PageRank algorithm using two methods: a random surfer model (sampling) and an iterative calculation approach. The aim is to understand and simulate how search engines rank pages based on their importance derived from linking structures.

## Description

The PageRank algorithm assigns a numerical weighting to each element of a hyperlinked set of documents, such as the World Wide Web, with the purpose of "measuring" its relative importance within the set. This implementation showcases two distinct approaches:

1. **Random Surfer Model (Sampling Method)**: Simulates the behavior of a web surfer who randomly clicks on links.
2. **Iterative Algorithm**: Uses a recursive mathematical formula to compute the PageRank of each page iteratively.

## Project Structure

- `pagerank.py`: Contains the main implementation of the PageRank algorithm.
- `corpus/`: A directory that can contain subdirectories of HTML files representing different corpuses on which to run the algorithm.

## Setup and Running the Code

### Prerequisites

- Python 3.6 or higher
- No external libraries are required for the basic functionality.

### Instructions

1. **Clone the Repository**: Start by cloning the repository to your local machine.


2. **Navigate to the Project Directory**:


3. **Run the Script**: To run the PageRank algorithm, you need to pass the directory containing your corpus as an argument.


Output will display the estimated PageRank for each HTML file in the specified corpus directory.

## Understanding the Output

The output consists of two parts:

- **PageRank Results from Sampling (n=10000)**: Shows the PageRank of each page as estimated by randomly sampling 10,000 surfer positions.
- **PageRank Results from Iteration**: Displays the PageRank as calculated through the iterative method.

