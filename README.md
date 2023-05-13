# GoogleDriveConnector

### Built With

- FastAPI (api)
- pydantic (data model)
- googleapiclient (connect google drive)
- google.oauth2 (authen with google)
- pytest (test)

### How do I get set up?

- download google service account ("service_account.json") and put in credentials folder
- if you want in local 
  ```
  make setup
  ```

### Usage (Server)

- start (local)
  ```
  make api_start
  ```
- start (docker)
  ```
  make docker_build
  make docker_run
  ```
- integration test (local)
  ```
  make integration test
  ```

### How does it work

- use google client api to retrieve folder structure and file content and transform to expect format
- it's support 2 type or shared_url
  - shared_url with without restricted (everybody have link can access it)
    - in this url type user cant copy and send url to api
  - shared_url with restrcted (only user who have permission can access it)
    - in this url type user have to share read permission to service account before send url to api 
### Edge Cases
- [x] missing query params
  - handled by return http_status_code 422
- [x] invalid url or url cant access
  - handled by return http_status_code 400
- [x] big files 
  - handled by read only file that siz <= config.to_read_content_size_threshold 
- [ ] have alot of files or deep nested
  - didn't handled currently it will time out
  - expect handle by async update to db instead response
