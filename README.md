# Proiect IDP

Acest proiect reprezinta o aplicatie de rezervare intr-un hotel folosind diferite servicii dezvoltate intr-un sistem folosind containere Docker.

## Servicii utilizate
1. Baza de date

Contine tabele pentru camerele din hotel si rezervarile efectuate.

2. Adaptor pentru baza de date

Un wrapper peste serviciul de baza de date pentru a expune interfetelor destinate clientilor si administratorilor operatii mai simple de folosit si de inteles.

3. Interfata de rezervare pentru clienti

Interfata web unde clientii pot vedea camerele din hotel si pot face o rezervare.

4. Interfata de administrare pentru proprietarii hotelului

Interfata web unde administratorii pot vedea rezervarile efectuate, pot schimba date, pot schimba/adauga camere, etc.

5. Monitorizare diferite statistici

Serviciu ce monitorieaza diferite statistici despre hotel precum gradul de ocupare, cele mai ocupate zile, camere preferate, etc.

## Schema serviciilor
![Schema serviciilor](./assets/img/schema_servicii.png?raw=true "Schema serviciilor")
