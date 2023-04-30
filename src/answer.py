import sys
import torch
from transformers import AutoTokenizer, AutoModelForQuestionAnswering

# Load BERT tokenizer and model
tokenizer = AutoTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
model = AutoModelForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')

def divideArticle(articleText, chunkSize=512, overlap=0):
    """
    Function to divide an article text into chunks of specified size with an overlap.

    Args:
    - articleText (str): The input article text as a string.
    - chunkSize (int): The maximum size of each chunk in terms of tokens. Default is 512.
    - overlap (int): The overlap size between consecutive chunks in terms of tokens. Default is 0.

    Returns:
    - list: A list of article chunks as strings.
    """
    # Tokenize the article into words
    words = articleText.split()
    
    # Initialize a list to store the article chunks
    chunks = []
    
    # Initialize variables to keep track of the current chunk and token count
    current_chunk = ""
    current_token_count = 0

    next_chunk = ""
    next_token_count = 0
    
    # Iterate through each word in the article
    for word in words:
        # Get the number of tokens for the current word
        num_tokens = len(tokenizer.tokenize(word))
        
        # If adding the current word to the current chunk would exceed the max tokens,
        # append the current chunk to the list of chunks and start a new chunk
        if current_token_count + num_tokens > chunkSize:
            chunks.append(current_chunk)
            current_chunk = next_chunk
            current_token_count = next_token_count
            next_chunk = ""
            next_token_count = 0
        
        # Add the current word to the current chunk
        current_chunk += word + " "
        current_token_count += num_tokens + 1  # Add 1 for the space after the word

        # Keep track of the words creating the overlapping tokens with the next chunk
        if (current_token_count + overlap > chunkSize):
            next_chunk += word + " "
            next_token_count += num_tokens + 1
        
    # Append the last chunk to the list of chunks
    chunks.append(current_chunk)
    
    return chunks

def validAnswer(answer):
    """
    Function to check if an answer string is valid.

    Args:
    - answer (str): The input answer string.

    Returns:
    - bool: True if the answer is valid, False otherwise.
    """
    if not answer:
        return False
    
    if "[SEP]" in answer \
    or "[CLS]" in answer \
    or "[MASK]" in answer:
        return False
    
    return True

# Function to evaluate a question and find the most correct answer across multiple article chunks.
def evaluateQuestion(question, articleChunks):
    """
    Args:
    - question (str): The input question as a string.
    - articleChunks (list): The list of article chunks as strings.

    Returns:
    - str: The most correct answer found in the article chunks, or 'No answer found.' if no answer is found.
    """

    # Initialize variables to store the maximum score and the corresponding answer
    max_score = float('-inf')
    best_answer = ""

    # Iterate through each article chunk
    for articleChunk in articleChunks:

        # Tokenize the question and article chunk
        inputs = tokenizer.encode_plus(question, articleChunk, add_special_tokens=True, return_tensors='pt')

        # Get the model's predictions for the start and end positions of the answer
        start_scores, end_scores = model(**inputs).values()

        # Find the start and end positions with the highest scores
        answer_start = torch.argmax(start_scores)
        answer_end = torch.argmax(end_scores) + 1

        # Get the answer text from the article chunk
        answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(inputs['input_ids'][0][answer_start:answer_end]))

        # Calculate the sum of start and end scores as the score for the answer
        score = start_scores[0][answer_start] + end_scores[0][answer_end - 1]

        # Update the maximum score and the corresponding answer if necessary
        if score > max_score:
            max_score = score
            best_answer = answer

    # Return the most correct answer found across all the article chunks
    if not validAnswer(best_answer):
        return "No answer found."
    return best_answer


# Function to perform question answering on an article given a list of questions
def questionAnswering(article, questions):
    """
    Args:
    - article (str): The file path to the article file.
    - questions (str): The file path to the questions file.

    Returns:
    - None
    """

    # Load article file
    with open(article, 'r') as f:
        articleText = f.read()

    # Load questions file
    with open(questions, 'r') as f:
        questions = f.readlines()

    # create the chunks from the article based on the maximum number of tokens the BERT model can handle
    articleChunks = divideArticle(articleText, overlap=50)

    # evaluate each question on all chunks to produce an answer
    for question in questions:
        question = question.strip() # Remove newline character
        answer = evaluateQuestion(question, articleChunks)
        print(answer)


# Call the question answering system with the command line arguments
questionAnswering(sys.argv[1], sys.argv[2])