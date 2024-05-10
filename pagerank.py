import os
import random
import re
import sys

DAMPING = 0.85  # The damping factor is used to model the probability that a surfer follows a link.
SAMPLES = 10000  # Number of samples used in the Monte Carlo method for estimating PageRank.

def main():
    # Check if the correct number of command-line arguments are given.
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    # Crawl the directory and build a corpus dictionary where keys are page names and values are sets of linked pages.
    corpus = crawl(sys.argv[1])
    # Calculate PageRank using the random sampling method.
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    # Calculate PageRank using the iterative method.
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")

def crawl(directory):
    """
    Parse a directory of HTML pages and extract links within those pages.
    Returns a dictionary mapping each page to a set of pages it links to.
    """
    pages = dict()
    # List all files in the directory and process HTML files.
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            # Use regex to find links within the page.
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            # Remove self-links and store in the dictionary.
            pages[filename] = set(links) - {filename}

    # Ensure all links in values are pages actually present in the directory.
    for filename in pages:
        pages[filename] = set(link for link in pages[filename] if link in pages)

    return pages

def transition_model(corpus, page, damping_factor):
    """
    Calculate PageRank for each page using the iterative approach and return the PageRank values.
    
    Args:
        corpus (dict): The corpus of web pages.
        damping_factor (float): The damping factor.
        convergence_threshold (float): The threshold for determining convergence.
        
    Returns:
        dict: The PageRank for each page.
    """

    N = len(corpus)
    distribution = dict.fromkeys(corpus, (1 - damping_factor) / N)

    links = corpus[page]
    if links:
        link_probability = damping_factor / len(links)
        for link in links:
            distribution[link] += link_probability
    else:
        # If no outgoing links, treat it as having a link to every page (including itself).
        for pg in corpus:
            distribution[pg] += damping_factor / N

    return distribution

def sample_pagerank(corpus, damping_factor, n):
    """
    Estimate the PageRank of each page by sampling pages according to the random surfer model.
    
    Args:
        corpus (dict): The corpus of web pages.
        damping_factor (float): The damping factor used in the transition model.
        n (int): The number of samples to generate.
        
    Returns:
        dict: Estimated PageRank for each page.
    """
    page_rank = dict.fromkeys(corpus, 0)
    page = random.choice(list(corpus.keys()))  # Start sampling from a random page.
    page_rank[page] += 1

    for _ in range(1, n):
        current_distribution = transition_model(corpus, page, damping_factor)
        page = random.choices(list(current_distribution.keys()), weights=current_distribution.values(), k=1)[0]
        page_rank[page] += 1

    # Normalize the results to probabilities.
    for page in page_rank:
        page_rank[page] /= n

    return page_rank

def iterate_pagerank(corpus, damping_factor):
    """
    Calculate PageRank values using an iterative algorithm until convergence.
    """
    N = len(corpus)
    page_rank = dict.fromkeys(corpus, 1 / N)
    change_threshold = 0.001  # Convergence threshold.
    change = True

    while change:
        change = False
        new_rank = {}
        for page in corpus:
            rank_sum = 0
            for possible_linker in corpus:
                if page in corpus[possible_linker]:
                    rank_sum += page_rank[possible_linker] / len(corpus[possible_linker])
                if not corpus[possible_linker]:  # Handle pages with no links.
                    rank_sum += page_rank[possible_linker] / N
            new_page_rank = (1 - damping_factor) / N + damping_factor * rank_sum
            if abs(new_page_rank - page_rank[page]) > change_threshold:
                change = True
            new_rank[page] = new_page_rank
        page_rank = new_rank

    return page_rank


if __name__ == "__main__":
    main()
