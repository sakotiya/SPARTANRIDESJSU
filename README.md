# SPARTANRIDESJSU
## Introduction 
The Spartan Ride is a fully developed, campus-based ride-sharing platform designed to improve transportation accessibility for members of the San José State University community. Tailored to the needs of both students and faculty, the system offers a reliable, affordable, and university-operated alternative to commercial ride-hailing services, focusing on short-distance travel within and around campus.
The platform provides a streamlined digital interface through which users can easily request rides, whether commuting between campus buildings, connecting to nearby transit hubs, or attending local events. It emphasizes simplicity, transparency, and role-based access to ensure that each user group—students, faculty, drivers, and administrators—can interact with the system according to their specific needs.

The Spartan Ride is built on a carefully normalized relational database that underpins the platform’s reliability, efficiency, and scalability. From the initial design phase, the database schema was structured with industry-standard best practices, ensuring referential integrity, data consistency, and logical clarity across all entities.
Normalization principles were rigorously applied to eliminate data redundancy and ensure that each table, such as student, driver, route, booking, and trip_history, serves a distinct and cohesive purpose. By defining clear foreign key relationships between tables (e.g., linking booking to both user and route), the system minimizes duplication and facilitates accurate, real-time queries without performance bottlenecks.

## Data Sources
Most of the tables used in the Spartan Ride were initially generated using Mockaroo (https://www.mockaroo.com), which allowed for quick prototyping of relational data through its table fabrication tools. These mock datasets provided a strong foundation for populating the operational database during development and UI testing.
However, Mockaroo's limitations—such as constraints on cross-table relationships, large-scale batch generation, and text diversity—made it difficult to simulate more dynamic or contextual data like trip logs, feedback content, or behavioral history. To address these gaps, the team utilized the educational version of GPT to generate supplementary data. This allowed for the creation of thousands of additional entries, enriched with more varied booking patterns, feedback messages, and route activity, ultimately enhancing the depth and realism of the system’s dataset.
By combining Mockaroo’s schema-driven data generation with GPT’s language-based synthesis, the team was able to produce a comprehensive dataset suitable for both functional implementation and analytical testing. 

## Application Design
The tools used during development include Python, MySQL Workbench, PyQt Designer, ERD Plus, and Jupyter Notebook. It requires additional packages to be installed:
● Pandas
● Numpy
● Matplotlib
● PyQt5 and PyQt5-Tools
● Seaborn
● MySQL Connector for Python

## Operational Module

The Operational Module of the Spartan Ride serves as the core engine for day-to-day campus transportation activities. It supports three primary user roles—riders (students and faculty), drivers, and administrators—each with a dedicated interface tailored to their tasks and responsibilities.
Riders can seamlessly sign up, log in, and book rides through an intuitive interface. They are able to choose from available routes, select a specific stop and time, and confirm their reservation with a single click. In addition to scheduling rides, riders can view their trip history, leave feedback with optional star ratings, and monitor their wallet balance. The Profile page allows them to verify or update their contact details. All ride activities are logged with timestamps and status indicators, enabling transparent record-keeping and accountability.
Drivers use the operational module to access and manage their daily assignments. After logging in, drivers can view their assigned routes, track upcoming stops, and update the real-time status of ongoing rides. The My Routes page provides a breakdown of stop names, scheduled times, and passenger counts. The Trip Logs feature summarizes weekly driving activity and estimates total working minutes and salary, while the Notifications section displays rider-submitted feedback related to their recent trips. This structured workflow helps drivers stay organized and performance-aware.
Administrators are provided with a centralized control panel to oversee system-wide operations. Through role-specific dashboards, they can monitor ride volumes, booking trends, and user activity across students, faculty, and drivers. Admins also have access to data entry and maintenance screens, where they can view, edit, or delete user records. These tools enable them to ensure service reliability, balance resource allocation, and address user-reported issues effectively.
By tightly integrating rider services, driver operations, and administrative oversight, the Operational Module ensures seamless scheduling, real-time coordination, and continuous performance tracking. It forms the backbone of the Spartan Ride platform, supporting reliable, scalable, and role-aware transportation across the campus. 

## Analytical Module
The analytical module supports administrators and university decision-makers by transforming operational data into actionable insights. Data collected through the operational database—including ride bookings, route selections, feedback ratings, and driver performance—is regularly extracted, cleaned, and structured into an analytical data warehouse. Using a STAR schema design, the module enables time-based, user-based, and route-based analysis. This supports use cases such as tracking peak hours, identifying underused routes, and evaluating service satisfaction trends. The insights are visualized through dashboards, allowing administrators to optimize operations and plan resource allocation effectively.

## Database Design
The Spartan Ride is built on a carefully normalized relational database that underpins the platform’s reliability, efficiency, and scalability. From the initial design phase, the database schema was structured with industry-standard best practices, ensuring referential integrity, data consistency, and logical clarity across all entities.
Normalization principles were rigorously applied to eliminate data redundancy and ensure that each table, such as student, driver, route, booking, and trip_history, serves a distinct and cohesive purpose. By defining clear foreign key relationships between tables (e.g., linking booking to both user and route), the system minimizes duplication and facilitates accurate, real-time queries without performance bottlenecks.
This clean, modular schema improves maintainability: developers can easily extend the system, for instance, by adding a new user role, expanding the route network, or integrating additional analytics modules, without restructuring existing tables. It also simplifies debugging and future-proofing, as updates or schema migrations can be performed with minimal disruption.
As a result, the database remains both lightweight and scalable, capable of handling increased user volume and data complexity while preserving responsiveness. This architecture supports all operational modules—rider booking, driver coordination, admin dashboards—as well as analytical processes such as ETL and dashboard visualizations.
By balancing structural rigor with flexibility, the Spartan Ride database provides a stable foundation for long-term growth, system reliability, and evolving institutional needs.

## Working of the Operational Module
The Spartan Ride is structured around three key user roles: Rider, Driver, and Administrator. Each role is equipped with features tailored to its responsibilities, enabling efficient coordination and seamless operation of campus ride services.
The Rider role includes both students and faculty members who use the platform to book rides around campus and nearby areas. Riders can log in to schedule rides, review their ride history, and submit feedback. Additionally, they can access a personal profile page where they can view and manage their account details and check the current status of their wallet balance, which reflects ride credits or payments made within the platform. These tools provide transparency and control, ensuring a smooth and personalized experience for every rider.
The Driver plays a central role in the operational flow of the system. Drivers can view their assigned routes and update ride statuses in real time. They can also access their ride log to track past trips and check a personal profile page that includes detailed information such as contact info and vehicle data. Importantly, drivers can review their salary information and see the ratings and feedback they've received from riders, giving them insight into their performance and helping them maintain high-quality service.
The Administrator oversees system usage and monitors overall performance. While not directly involved in ride execution, administrators use analytics dashboards to track system activity, including ride volume and usage patterns by time and region. These insights support data-driven decision-making and operational improvements.


## Working of the Analytical Module
Operational data is extracted from the live database and loaded into an analytical data warehouse using scheduled ETL pipelines. The data is transformed to match the STAR schema format, with a central fact table (e.g., trips or bookings) and supporting dimension tables (e.g., time, route, user). This structure allows for flexible slicing and dicing of the data. For instance, administrators can analyze total rides by hour, week, or region, and correlate feedback trends with specific drivers or time windows. These metrics are used for service optimization and planning.

<img width="555" alt="Screenshot 2025-06-03 at 8 04 16 PM" src="https://github.com/user-attachments/assets/61e1d8e0-38c3-48ce-8b46-fd443324915c" />


<img width="726" alt="Screenshot 2025-06-03 at 8 04 36 PM" src="https://github.com/user-attachments/assets/b3061f0a-3c75-4b83-a212-29fcf529ed20" />



# SPARTANRIDESJSU
To run application 
1. Connect to Remote server
2. User terminal to go to project folder
3. Run following command

````SPARTANRIDESJSU % python -m SourceCode.Login_Page````

