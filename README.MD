# That Random Streamer!
![chaosgorilla](./streamer.jpg)

This server will create radomn streams of data that you can use in challenges or tests.

## Stream that Data
These 3 APIs return 3 data streams. Call them and combine their data together in a timely manner.

From this data:
- Clean and standardize data.
- Find the most common letter.
- Plot the use of this letter through out time.

## Data Stream APIs.
- GET | /stream1</li>
- GET | /stream2</li>
- GET | /stream3</li>

### [GET]/streamX
Part of 3 data streams.

Responses:
- 200 - A Json object.</li>
- 400 - Required data not available.</li>
- 429 - Rate limit reached.</li>
- 500 - An Internal error.</li>

The JSON Payload: `application/json`

- "id": number, e.g.- 1
- "date": datatime, e.g. - "10/27/2004, 02:07:56 AM"
- "payload": string or null, e.g. - "asdase3234df"
