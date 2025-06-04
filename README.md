# SPARTANRIDESJSU
Introduction 
The Spartan Ride is a fully developed, campus-based ride-sharing platform designed to improve transportation accessibility for members of the San José State University community. Tailored to the needs of both students and faculty, the system offers a reliable, affordable, and university-operated alternative to commercial ride-hailing services, focusing on short-distance travel within and around campus.
The platform provides a streamlined digital interface through which users can easily request rides, whether commuting between campus buildings, connecting to nearby transit hubs, or attending local events. It emphasizes simplicity, transparency, and role-based access to ensure that each user group—students, faculty, drivers, and administrators—can interact with the system according to their specific needs.

The Spartan Ride is built on a carefully normalized relational database that underpins the platform’s reliability, efficiency, and scalability. From the initial design phase, the database schema was structured with industry-standard best practices, ensuring referential integrity, data consistency, and logical clarity across all entities.
Normalization principles were rigorously applied to eliminate data redundancy and ensure that each table, such as student, driver, route, booking, and trip_history, serves a distinct and cohesive purpose. By defining clear foreign key relationships between tables (e.g., linking booking to both user and route), the system minimizes duplication and facilitates accurate, real-time queries without performance bottlenecks.

Data Sources
Most of the tables used in the Spartan Ride were initially generated using Mockaroo (https://www.mockaroo.com), which allowed for quick prototyping of relational data through its table fabrication tools. These mock datasets provided a strong foundation for populating the operational database during development and UI testing.
However, Mockaroo's limitations—such as constraints on cross-table relationships, large-scale batch generation, and text diversity—made it difficult to simulate more dynamic or contextual data like trip logs, feedback content, or behavioral history. To address these gaps, the team utilized the educational version of GPT to generate supplementary data. This allowed for the creation of thousands of additional entries, enriched with more varied booking patterns, feedback messages, and route activity, ultimately enhancing the depth and realism of the system’s dataset.
By combining Mockaroo’s schema-driven data generation with GPT’s language-based synthesis, the team was able to produce a comprehensive dataset suitable for both functional implementation and analytical testing. 2

<img width="555" alt="Screenshot 2025-06-03 at 8 04 16 PM" src="https://github.com/user-attachments/assets/61e1d8e0-38c3-48ce-8b46-fd443324915c" />


<img width="726" alt="Screenshot 2025-06-03 at 8 04 36 PM" src="https://github.com/user-attachments/assets/b3061f0a-3c75-4b83-a212-29fcf529ed20" />



# SPARTANRIDESJSU
To run application 
1. Connect to Remote server
2. User terminal to go to project folder
3. Run following command

````SPARTANRIDESJSU % python -m SourceCode.Login_Page````

