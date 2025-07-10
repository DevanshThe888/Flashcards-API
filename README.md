# 🧠 Flashcard API

A lightweight RESTful API to manage flashcards for spaced repetition learning. Users can create, retrieve, update, and delete flashcards with difficulty tags (`RED`, `YELLOW`, `GREEN`), and track their learning activity with a visual usage heatmap.

---

## 🔧 Features

- Create flashcards with question, answer, and difficulty tag
- Retrieve flashcards by ID, all, or filtered by tag
- Partial updates using PATCH
- In-memory storage (no external DB)
- View usage heatmap with calendar-style visualization

---

## 🌐 Base URL

http://localhost:5000/

---

## ⚙️ Local Setup

Follow these steps to run the project locally:

### 🔁 Clone the Repository

```bash
git clone <your-repo-url>
cd <project-folder>
```

### 📦 Install Dependencies

```bash
pip install -r requirements.txt
```
### 🚀 Run the Server

```bash
python main.py
```

By default, the app runs on `http://localhost:5000/`

---

## 🔐 Authentication

No authentication is required for this API.

All endpoints are public and intended for local/test usage only.

---




## 📁 Endpoints Reference

### 1. Create a Flashcard
- **HTTP Verb**: `POST`
- **URL**: `/postFlashcard`
- **Purpose**: Create a new flashcard.
- **Request Body (JSON)**:
  ```json
   {
    "question": "What is the capital of France?",
    "answer": "Paris",
    "tag": "GREEN"
   }
   
  ```
 - **Success Response**: `201 Created` + JSON with generated id
   ```json
    {
	 "id": 0, 
	 "question": "What is the capital of France?", 
	 "answer": "Paris", 
	 "tag": "GREEN"
    }
    
    ```
- Error Responses: 
  - `400 Bad Request` if `question`/`answer`/`tag` is missing
  - `400 Bad Request` if `tag` is invalid
  - `400 Bad Request` if `question` already exists


### 2. Retrieve All Flashcards
- **HTTP Verb**: `GET`
- **URL**: 
	- `/get_allFlashcards`  
	- `/get_allFlashcards?reveal=true` 
- **Purpose**: Get all flashcards (answers hidden by default)
 - **Optional Query Parameter**:  `reveal=true`: Show answers (`reveal=yes`/`1` also works)
 - **Success Response**: `200 OK` + List of flashcards (without answers unless revealed)
   ```json
	[
	  {
	    "id": 0,
	    "question": "What is the capital of France?",
	    "answer": "Paris",
	    "tag": "GREEN"
	  },
	  {
	    "id": 1,
	    "question": "Who's the Prime Minister of India?",
	    "tag": "GREEN"
	  },
	  {
	    "id": 2,
	    "question": "What is the capital of Canada?",
	    "tag": "RED"
	  },
	  {
	    "id": 3,
	    "question": "What planet is known as the Red Planet?",
	    "tag": "YELLOW"
	  },
	  {
	    "id": 4,
	    "question": "2 + 2 + 2 + 2 + 2 =",
	    "tag": "RED"
	  }
	]
	
    ```
    ### 4. Retrieve a Single Flashcard

-   **HTTP Verb**: `GET`
-   **URL**: `/getFlashcard/<int:flashcard_id>`
-   **Purpose**: Get a flashcard by its ID
-   **Optional Query Parameter**:
    -   `reveal=true`: Show answer
-   **Success Response**:
    -   `200 OK` + Flashcard data:

```json
  {
	"id": 1, 
	"question": "...", 
	"tag": "GREEN"
  }  // No answer unless revealed
  
```
-   **Error Response**:
    -   `404 Not Found` if `flashcard_id` doesn't exist
### 5. Update a Flashcard

-   **HTTP Verb**: `PATCH`
-   **URL**: `/patchFlashcard/<int:flashcard_id>`
-   **Purpose**: Update a flashcard (partial updates allowed)
-   **Request Body (JSON)**:

```json
  {
	"question": "Updated question?",
	"answer": "Updated answer",
	"tag": "YELLOW"  
  } // Optional fields
  
```

-   **Success Response**:
    -   `200 OK` + `{"message": "updated"}`
-   **Error Responses**:
    -   `404 Not Found` if `flashcard_id` doesn't exist
    -   `400 Bad Request` for duplicate questions or invalid tags

### 6. Delete a Flashcard

-   **HTTP Verb**: `DELETE`
-   **URL**: `/deleteFlashcard/<int:flashcard_id>`
-   **Purpose**: Delete a flashcard by ID
-   **Success Response**:
    -   `204 No Content` (empty body)
-   **Error Response**:
    -   `404 Not Found` if `flashcard_id` doesn't exist

### 7. Activity Heatmap

-   **HTTP Verb**: `GET`
-   **URL**: `/heatmap`
-   **Purpose**: Generate a heatmap PNG of user activity (days with API calls)
-   **Success Response**:
    -   `200 OK` + PNG image
-   **How It Works**:
    -   Tracks every `GET`/`POST`/`PATCH` request to flashcard endpoints
    -   Colors represent request volume per day (darker = more requests)
 ---

## 📐 Flashcard Data Schema

A flashcard object has the following structure:

```json
{
  "id": 0,
  "question": "What is the capital of France?",
  "answer": "Paris",
  "tag": "GREEN"
}

```

 | Field     | Type   | Required | Description                                                    |
|-----------|--------|----------|----------------------------------------------------------------|
| `id`      | int    | No       | Auto-generated unique identifier                               |
| `question`| string | Yes      | The question text                                              |
| `answer`  | string | Yes      | The answer text (optional to reveal in GET requests)           |
| `tag`     | string | Yes      | Must be one of: `RED`, `YELLOW`, `GREEN` (case-insensitive)    |
---

## 🧪 Testing the API in Postman

To test this API:

- Import the complete Postman Collection from here - 
	-[Download Postman Collection 1 - POST requests](./POST_requests.postman_collection.json)
	-[Download Postman Collection 2 - GET, PATCH, DEL, heatmap requests](./GET_DEL_PATCH_requests.postman_collection.json)

> 📌 To import: 
> 1.  Open Postman   
> 2.  Click **Import**  
> 3.  Upload the `.json` file
---

## 🚨 Error Codes

The API returns standard HTTP error responses in the following scenarios:

| Code | Message Example                                   | Cause                                  |
|------|---------------------------------------------------|----------------------------------------|
| 400  | "Choose one amongst RED, YELLOW, or GREEN"        | Invalid `tag` in request               |
| 400  | "Question already exists at flashcard_id: 3"      | Duplicate question                     |
| 400  | "Missing required fields"                         | `question`, `answer`, or `tag` missing |
| 404  | "Flashcard not found."                            | Flashcard with given ID doesn’t exist  |

## 👥 Maintainers

This project is not actively maintained.

## 📜 License

This project is licensed under the **MIT License**.  
See the [LICENSE](./LICENSE) file for details.
