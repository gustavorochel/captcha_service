# CAPTCHA API


 API gateway to receive captcha images and detect them.


## Installation

### Configuration

Create a file named .env and copy the content of env.example file.
Fill out all information about db and models.

#### Build and run containers

If it is necessary give execution permision to the docker-init.sh file.

```bash
sudo chmod +x docker-init.sh
```

In the root directory run the [docker-compose](https://docs.docker.com/compose/):

## Run it

With the images builded, run the docker-compose:

```bash
docker-compose up  
```

## Get captcha route

```bash
<host-id>:<port>/api/v1/model/predict_captcha
```
## Input interface

```bash
{
    "base_64_image": "Base64 Image",
}
```

## Output interface

```bash
{
    "captcha_value": "99999"
}
```