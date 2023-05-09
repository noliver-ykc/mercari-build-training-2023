# STEP3: Make a listing API

## 1. Call an API

**:book: Reference**

* (JA) [Udemy Business - REST WebAPI サービス 設計](https://mercari.udemy.com/course/rest-webapi-development/)
* (JA) [HTTP レスポンスステータスコード](https://developer.mozilla.org/ja/docs/Web/HTTP/Status)
* (JA) [HTTP リクエストメソッド](https://developer.mozilla.org/ja/docs/Web/HTTP/Methods)
* (JA) [APIとは？意味やメリット、使い方を世界一わかりやすく解説](https://www.sejuku.net/blog/7087)

* (EN) [Udemy Business - API and Web Service Introduction](https://mercari.udemy.com/course/api-and-web-service-introduction/)
* (EN) [HTTP response status codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)
* (EN) [HTTP request methods](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods)

### GET request

In step2, you ran a service on your local server where you accessed the endpoint from `http://127.0.0.1:9000` using your browser.
Use the following `curl` command to access this endpoint. Install `curl` if necessary.

```shell
curl -X GET 'http://127.0.0.1:9000'
```

Check if you can see `{"message": "Hello, world!"}` on your console.

### POST request.

In the example implementation, you can see `/items` endpoint. Use `curl` to call this endpoints.

```shell
$ curl -X POST 'http://127.0.0.1:9000/items'
```

This endpoint expects to return `{"message": "item received: <name>"}`, but you should be seeing something different.

Modify the command as follows and see that you receive `{"message": "item received: jacket"}`. Investigate what causes the differences.

```shell
$ curl -X POST \
  --url 'http://localhost:9000/items' \
  -d name=jacket
```

**:beginner: Points**

* Understand the difference betweeen GET and POST requests.
* Why do we not see `{"message": "item received: <name>"}` on accessing `http://127.0.0.1:9000/items` from your browser?
  * What is the **HTTP Status Code** when you receive these responses?
  * What do different types of status code mean?

NOTES FROM NICOLE:
Understand the difference between GET and POST requests:

 * GET: The GET method is used to request data from a specified resource (e.g., a URL). It doesn't submit or change any data on the server. GET requests are idempotent, meaning that making the same request multiple times will yield the same result. They should only be used for retrieving data.
 * POST: The POST method is used to submit data to a specified resource for processing, usually to create or update a resource. It sends data to the server in the request body. POST requests are not idempotent, so making the same request multiple times may have different outcomes.

Why do we not see {"message": "item received: <name>"} on accessing http://127.0.0.1:9000/items from your browser?
 * When you access a URL in your browser, it sends a GET request by default. The /items endpoint in the FastAPI application is defined to respond to POST requests. To see the expected response, you must send a POST request to the endpoint, which can be done using tools like curl, Postman, or by writing code to send the request.

What is the HTTP Status Code when you receive these responses?
 * For a successful POST request to the /items endpoint, the HTTP status code will be 200 OK. This status code indicates that the request was successful and the server has returned the requested data.
 * If you try to access the /items endpoint with a GET request (e.g., from your browser), you'll receive a 405 Method Not Allowed status code, which means the HTTP method used is not supported for the requested resource.

What do different types of status codes mean?
 * HTTP status codes are three-digit numbers that indicate the outcome of an HTTP request. They are grouped into five classes based on the first digit:
 * 1xx (Informational): The request was received, and the server is continuing to process it.
 * 2xx (Successful): The request was successfully received, understood, and accepted.
 * 3xx (Redirection): The request needs further action to be completed, usually following a provided URL.
 * 4xx (Client Error): The request contains bad syntax or cannot be fulfilled by the server.
 * 5xx (Server Error): The server failed to fulfill a valid request.
_Some common status codes include:_
 * 200 OK: The request was successful, and the server has returned the requested data.
 * 201 Created: The request was successful, and the server has created a new resource as a result.
 * 400 Bad Request: The server cannot process the request due to incorrect syntax or invalid data.
 * 401 Unauthorized: The request requires authentication, and the client has not provided valid credentials.
 * 403 Forbidden: The client does not have permission to access the requested resource.
 * 404 Not Found: The requested resource could not be found on the server.
 * 500 Internal Server Error: The server encountered an error while processing the request.


## 2. List a new item

Make an endpoint to add a new item

**:book: Reference**

* (JA)[RESTful Web API の設計](https://docs.microsoft.com/ja-jp/azure/architecture/best-practices/api-design)
* (JA)[HTTP レスポンスステータスコード](https://developer.mozilla.org/ja/docs/Web/HTTP/Status)
* (EN) [RESTful web API design](https://docs.microsoft.com/en-us/azure/architecture/best-practices/api-design)
* (EN) [HTTP response status codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)

The endpoint already implemented (`POST /items`) takes `name` as an argument. Modify the API such that it also accepts `category` informaton.

* name: Name of the item (string)
* category: Category of the item (string)

Since the information cannot be retained with the current implementation, save this into a `JSON` file.
Make a file called `items.json` and add new items under `items` key.

`items.json` is expected to look like the following.
```json
{"items": [{"name": "jacket", "category": "fashion"}, ...]}
```

## 3. Get a list of items

Implement a GET endpoint `/items` that returns the list of all items. The response should look like the following.

```shell
# Add a new item
$ curl -X POST \
  --url 'http://localhost:9000/items' \
  -d 'name=jacket' \
  -d 'category=fashion'
# Expected response for /items endpoint with POST request
{"message": "item received: jacket"}
# Get a list of items
$ curl -X GET 'http://127.0.0.1:9000/items'
# Expected response for /items endpoint with GET request
{"items": [{"name": "jacket", "category": "fashion"}, ...]}
```

## 4. Add an image to an item

Change the endpoints `GET /items` and `POST /items` such that items can have images while listing.

* Make a directory called `images`
* Hash the image using sha256, and save it with the name `<hash>.jpg`
* Modify items such that the image file can be saved as a string

```shell
# POST the jpg file
curl -X POST \
  --url 'http://localhost:9000/items' \
  -F 'name=jacket' \
  -F 'category=fashion' \
  -F 'image=@images/local_image.jpg'
```

```json
{"items": [{"name": "jacket", "category": "fashion", "image_filename": "510824dfd4caed183a7a7cc2be80f24a5f5048e15b3b5338556d5bbd3f7bc267.jpg"}, ...]}
```


**:beginner: Point**

* What is hashing?
* What other hashing functions are out there except for sha256?


## 5. Return item details

Make an endpoint `GET /items/<item_id>` to return item details.

```shell
$ curl -X GET 'http://127.0.0.1:9000/items/1'
{"name": "jacket", "category": "fashion", "image": "..."}
```

## 6. (Optional) Understand Loggers
Open `http://127.0.0.1:9000/image/no_image.jpg` on your browser.
This returns an image called `no image` but the debug log is not displayed on your console.
```
Image not found: <image path>
```
Investigate the reason why this is the case. What changes should be made to display this message?

**:beginner: Points**
* What is log level?
* On a web server, what log levels should be displayed in a production environment?

---
**:beginner: Points**

Check if you understand the following concepts.

* port number
* localhost, 127.0.0.1
* HTTP request methods (GET, POST...)
* HTTP Status Code (What does each of 1XX, 2XX, 3XX, 4XX, 5XX mean?)

---

### Next

[STEP4: Database](04-database.en.md)
