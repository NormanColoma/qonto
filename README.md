# Qonto Test

## Language and Frameworks

I've used Python with Flask since it's a lightweight framework, and I've worked with it in the past Despite Python is not the 
language I'm most experienced with (which is Node+Javascript), I'm feel very comfortable working 
with it and since is one of the primaries languages at Qonto I wanted to show you that I'm capable.

## Project structure

The project has the standard DDD structure, with its corresponding layers:

* **Application**: This layer contains the application services. It is responsible for the coordination of the domain layer and the infrastructure layer.
* **Domain**: This layer contains the domain entities, it is the core of the application
* **Infrastructure**: This layer contains the implementation of the domain repositories and the external services.
 
Aside from those principal folders, you'll find the **test** folder, which contains the unit tests for all layers. 
In the **container.py** file you'll find the IoC container, which is used to inject the dependencies.

## Database

I've selected MySQL as a database for creating a more real scenario. There is an init.sql file which creates the schema and seed the
database (during docker-compose bootstrapping) with the account you provided in the samples (the one with the iban FR10474608000002006107XXXXX).

# Decisions and assumptions regarding the solution

As the requirements were well-defined and emphasizes on the importance of data consistency and atomicity, I've decided to handle the
update of the account balance and the creation of the transfer in a transactional way. Hence, if there's a failure during the transaction
our account state remains consistent, and this way we're also preventing another request modifies the account balance while it's a transaction
ongoing. This approach has the drawback that the larger the number of the transfer the longer we take, so we could end up with a performance 
problems depending on the number of the transfers, but as the requirements talks in order of hundreds, and it's an operation that it seems not 
to be frequently performed we could consider this solution in which we're choosing ACID principles over performance. I've done some test with
larger data than the examples given and in the order of hundreds the request takes around 500-800ms to complete, while in the order
of thousand it takes 1.5-3secs. To address potential performance bottlenecks, we could consider decoupling the creation of transfers from the transaction. 
By asynchronously creating transfers based on domain events, we can improve performance and reduce strain on the database. 
Nonetheless, this asynchronous approach introduces its own set of challenges, including event loss during transmission and handling failures in event consumption.

- What does happen if some of the events are lost during the transmission? 
- At consuming the event, what does happen if some transfer cannot be created? 
- If some events are not acknowledged, how many times are we going to try to resend them?  
- Would be weird for the user doing a transfer successfully and not seeing it?

Well, there's a lot of questions and problems that arise when we embrace eventual consistency that can be solved by applying 
saga pattern though is a harder scenario to deal with.

The trade-off between ACID principles and performance considerations ultimately depends on the specific requirements of the application. 
Conversations around these trade-offs are common when tackling complex problems, highlighting the importance of understanding and addressing the nuances of each solution.

# Improvements

* **Performance test**: In a real scenario having a performance test for foreseeing bottlenecks and performance issues is vital, but given
the time I had for doing the test I couldn't invest time on this topic.
* **Enhanced message broker**: I've added RabbitMQ as message broker for emitting events that usually are consumed from another 
bounded context, but in a real scenario we'll have to define a strategy for resending nacked messages (retries, interval between retries, dead letters...), 
creating multiple consumer and so on.
* **Transaction Optimizations**: If we would consider that the better approach fot this situation needs a higher isolation level and strategies 
for example preventing the table/row being read while there's another transaction using it, we could do it, but again it will be about
choosing one trade-off or another, because the higher is your isolation level the worst is your performance.
* **Error handling and logging**: Although the exceptions are being controlled and logged locally we could do some tweaks, for example publishing 
these errors to a real error monitoring service.
* **Monitoring, observability and tracing**: For the aim of simplicity I've not done anything on this, but is obvious than in a real scenario
we need to monitor our service, we need metrics for being able to assess how it's performing, traces for deep dive into an error.

# How to run the project

## Requirements

* Docker
* Docker Compose

## Steps

1. Run `docker-compose up` in the root folder. It will build the docker images (flask, MySQL, RabbitMq) and run them.
2. The server will be running on `http://localhost:5001`

### Feedback
**How much time did you spend performing this exercise?**

5h more or less

**How proud are you of your work?**

Fairly proud
