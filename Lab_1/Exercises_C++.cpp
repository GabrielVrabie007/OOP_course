#include <iostream>
#include <string>

using namespace std;

// 1. Encapsulation
class Person {
private:
    string name;
    int age;

public:
// Constructor with parameters
    Person(string name, int age) : name(name), age(age) {}

    string getName() { return name; }
    void setName(string n) { name = n; }

    // Getter and Setter for age
    int getAge() { return age; }
    void setAge(int a) { age = a; }

    ~Person() { // Destructor
        cout << "Destructor called for Person: " << name << endl;
    }
};

//Inheritance
class Employee : public Person {
private:
    double salary;

public:
    Employee(string name, int age, double salary) 
        : Person(name, age), salary(salary) {}

    double getSalary() { return salary; }
    void setSalary(double s) { salary = s; }

    ~Employee() {
        cout << "Destructor called for Employee" << endl;
    }
};

class Company; 

class Manager {

private:
    string department;

    friend void showManagerInfo(const Manager&, const Company&); 
    friend class Company; 

public:
    Manager(string dept) : department(dept) {}

    ~Manager() {
        cout << "Destructor called for Manager" << endl;
    }
};

class Company {
private:
    string companyName;

    //showManagerInfo--friend method
    friend void showManagerInfo(const Manager&, const Company&);

public:
    Company(string name) : companyName(name) {}

    ~Company() {
        cout << "Destructor called for Company" << endl;
    }

    void showDepartment(const Manager &m) {
        cout << "Manager's department: " << m.department << endl;
    }
};

void showManagerInfo(const Manager &m, const Company &c) {
    cout << "Manager's department: " << m.department << " | Company's name: " << c.companyName << endl;
}

int main() {
    // Encapsulation 
    Person person("Valera", 35);
    cout << person.getName() << " is " << person.getAge() << " years old." << endl;

    // Inheritance
    Employee emp("Bober", 40, 50000);
    cout << emp.getName() << " earns $" << emp.getSalary() << " annually." << endl;

    
    Manager manager("Sales");
    Company company("Wizz Air");


    company.showDepartment(manager);
    showManagerInfo(manager, company);

    return 0;
}

