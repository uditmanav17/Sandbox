# Super Hero App

This application was developed to get a better understanding of [FastApi](https://fastapi.tiangolo.com/), [SQLModel](https://sqlmodel.tiangolo.com/), [Docker/Compose](https://www.docker.com/). Original source code can be found [here](https://sqlmodel.tiangolo.com/tutorial/fastapi/simple-hero-api/).

-----

<details>
<summary><strong>Salient Features</strong></summary>
<br>

- **FastAPI** + **SQLModel** application development example
- Tests for application written using **pytest**
- Containerized using **Docker** multi-stage build
- **Postgres** service as backend database (compose mode)
- **Nginx** service as load balancer (compose mode) when scaling

</details>

-----

<details>
<summary><strong>Setting up</strong></summary>
<br>

**Software Requirement**
	- [Docker and docker-compose](https://docs.docker.com/compose/install/)
	- [Python + pytest](https://docs.pytest.org/en/6.2.x/getting-started.html) (optional - for testing only)

Running test cases
	- Navigate to `simple-hero-app`
	- In your terminal, execute `pytest`, all test cases should pass

**IMPORTANT** - Before proceeding to next section, rename `sample.env` to `.env`

</details>

------

<details>
<summary><strong>Starting application</strong></summary>
<br>

This application can be executed in 2 modes, both of which requires Docker installation on your system. 

- Start application in **Independent mode**
	- Navigate to `hero-app` directory
	- Build docker image using following command
		-  `docker build -t hero_app:v0 .`
		- This will create an image with name `hero_app` and tag `v0`
	- Run docker image 
		- `docker run -d -p 8080:8501 hero_app:v0`
		- This will start application on http://localhost:8080/ mapping host port 8080 to container port 8501, where application is actually running
	- In independent mode, dedicated DB is not available, so application uses **SQLite**. You can browse data in `sql-db/database.db` file using [DB Browser for SQLite](https://sqlitebrowser.org/)
 
- Start application in **Compose Mode**
	- Navigate to `simple-hero-app`
	- Spin up the Docker services using
		- `docker compose up -d --build`
		- This will build one instance of each service and start application on http://localhost:8081/
		- Bring down stack using - `docker compose down -v` also removing volumes containing all the DB data
	- Scaling services
		- `docker compose up -d --scale fast_heroes=5`
		- This will spin up 5 instances of `fast_heroes` service and `nginx` will redirect each request among these in round robin fashion
		- Application will be available at http://localhost:8081/ . Observe change in container ID after each refresh/request
	- Bring down stack 
	- In compose mode, you have `postgres` as a dedicated DB. If you want to browse data you'd need to attach shell to `postgres` service

</details>

------
