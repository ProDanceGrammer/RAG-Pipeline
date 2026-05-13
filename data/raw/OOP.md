# OOP

Skills: Architecture, OOP, Python
Start Date: March 9, 2026

# Terms

1. 

# OOP

**🔽 What? 🔽**

- paradigm in software development based on **objects** — software entities which are encapsulate **data and methods** in it**.**

**🔁 What does it do? 🔁**

- helps in code software development to build complex systems

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- **Encapsulation, inheritance and polymorphism** are main concepts of used **to increase** **modularity and flexibility** of code.

🤔 **How does it work?** 🤔

- Python is OOP language

**✍️ How to use it? ✍️**

- With defining the classes and their attributes with methods.

**👍 Advantages 👍**

- **Modularity**
- Code **Reusability**
- **Readability**
- **Extensibility**
- Ease to **maintain**
- Real-world modeling: objects represent real-world entities (e.g., `Car`, `User`, `BankAccount`), which makes system design more **intuitive**.

**👎 Disadvantages 👎**

- Requires a deep OOP knowledge
- More code / boilerplate – OOP often requires extra structure (classes, methods) compared to simpler approaches.
- **Performance overhead** – objects, method calls, and abstractions can be slower than simpler **procedural solutions**.

**↔️ Alternatives ↔️**

- Procedural programming
- Functional programming
- Data-oriented programming – prioritize efficient data structures and transformations rather than objects.
- Modular programming – structure programs into modules and functions without heavy use of classes.

**✅ Best practices ✅**

- Using SOLID principles
- **Composition over inheritance:** prefer combining objects instead of building deep inheritance trees.

**🛠️ Use cases 🛠️**

- Web Applications, Forms, ORMs, Games

**🛑 Worst practices 🛑**

- God classes: classes that try to handle **too many responsibilities**.
- **Deep inheritance hierarchies**: long chains like A → B → C → D → E, which make code hard to understand.
- Harder debugging – **deep inheritance** or **many interacting objects** can make bugs difficult to trace.
- Breaking encapsulation: **directly modifying internal attributes like obj._balance**.
- Using OOP when it’s unnecessary: sometimes a simple function or data structure is clearer.
- **Poor abstraction**: classes that expose **too many internal details** or depend heavily on other classes’ internals.

Sources:

## Classes and objects/instances

**🔽 What? 🔽**

- a blueprint

**🔁 What does it do? 🔁**

- uses in definition

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- to create a separeted object, with a behavior configured inside the class.

🤔 **How does it work?** 🤔

- 

**✍️ How to use it? ✍️**

- in OOP

**👍 Advantages 👍**

- 

**👎 Disadvantages 👎**

- 

**↔️ Alternatives ↔️**

- 

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- 

**🛑 Worst practices 🛑**

- 

Sources:

## Attributes

**🔽 What? 🔽**

- **Classes attributes** are variables that are shared across **all instances** of a class.
- **Instance attributes** are variables of a **specific one instance**. It may be distinguished with another instance of the same class. They are written in `__init__()` function.

**🔁 What does it do? 🔁**

- stores data

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- to store and hide data

🤔 **How does it work?** 🤔

- 

**✍️ How to use it? ✍️**

- 

**👍 Advantages 👍**

- 

**👎 Disadvantages 👎**

- 

**↔️ Alternatives ↔️**

- global variables

**✅ Best practices ✅**

- Use **class** attributes for **shared** data
    
    ```python
    class Car:
        wheels = 4   # class attribute
    ```
    
- **instance** attributes for **object-specific** data
- **Access class attributes** **through the class** when possible, but not instance.

**🛠️ Use cases 🛠️**

- 

**🛑 Worst practices 🛑**

- Using **mutable** objects as **class attributes** unintentionally
    
    ```python
    class A:
        items = []  # shared list for all instances (often a bug)
    
    # All instances will modify the **same** list.
    ```
    
- Accidentally **shadowing class attributes** with **instance** attributes
    
    ```python
    class A:
        value = 10
    
    a = A()
    a.value = 20  # now this exists only on this instance
    # This can confuse developers because A.value is still 10.
    ```
    
- Storing **instance-specific data** in **class** attributes
    
    ```python
    class User:
        name = None  # wrong place for per-object data
    # Each user should have its own name, so it should be in __init__.
    ```
    

Sources:

## Methods

**🔽 What? 🔽**

- behavior of objects which is defined as function in the class

**🔁 What does it do? 🔁**

- **Instance methods** operate on an instance of the class and have access to the instance(`self`) and its attributes.
- **Class methods** operate on the class itself. They are marked with `@classmethod` [decorator](https://www.notion.so/Python-319745f820dc80a4a8aad0e7083b88dc?pvs=21) and take `cls` as the first parameter. Can be used as **alternative constructors**.
- **Static methods** do **not** operate on the instance or the class. They are marked with a `@staticmethod` decorator and do not take `self` or `cls` as the first parameter. They are used for **utility** functions that **do not access class or instance data**.

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- to tell the code which actions it may do and how
- Instance methods
    - When the method needs to read or modify **instance** data.
    - When behavior depends on the state of a **specific object.**
- Class methods
    - When working with **class-level data.**
    - When creating **alternative constructors**.
- Static methods
    - Utility functions logically **related** to a class **but not dependent on instance or class data**.

🤔 **How does it work?** 🤔

- 

**✍️ How to use it? ✍️**

- Basic example
    
    ```python
    class Car:
        # Class attribute
        total_cars = 0
    
        def __init__(self, make, model, year):
            self.make = make
            self.model = model
            self.year = year
            Car.total_cars += 1  # Increment the total number of cars each time a new car is created
    
        # Instance method
        def description(self):
            """Returns a description of the car."""
            return f"{self.year} {self.make} {self.model}"
    
        # Class method
        @classmethod
        def total_cars_created(cls):
            """Returns the total number of cars created."""
            return f"Total cars created: {cls.total_cars}"
    
        # Static method
        @staticmethod
        def is_vintage(year):
            """Determines if a car is vintage based on its year."""
            return year < 1990
            
            
    # Creating car objects
    car1 = Car("Toyota", "Corolla", 1985)
    car2 = Car("Ford", "Mustang", 1968)
    
    # Using an instance method
    print(car1.description())  # Output: 1985 Toyota Corolla
    print(car2.description())  # Output: 1968 Ford Mustang
    
    # Using a class method
    print(Car.total_cars_created())  # Output: Total cars created: 2
    
    # Using a static method
    print(Car.is_vintage(1985))  # Output: True
    print(Car.is_vintage(1995))  # Output: False
    ```
    

**👍 Advantages 👍**

- 

**👎 Disadvantages 👎**

- 

**↔️ Alternatives ↔️**

- 

**✅ Best practices ✅**

- Instance methods
    - Use instance methods for **most object** behavior.
    - Modify or access attributes through `self`. not `this` or etc.
    - Keep methods focused on object responsibility.
- Class methods
    - Use them for [**factory methods](https://www.notion.so/Python-319745f820dc80a4a8aad0e7083b88dc?pvs=21)** (different ways to create objects).
    - Access class attributes through `cls`, not the class name.
    - Use when logic applies to the **whole class**, not a specific instance.
- Static methods
    - Use for **pure functions** that conceptually **belong to the class**.
    - Keep them **simple** and **independent of class** state.
    - Use when **grouping functionality** improves **readability**.

**🛠️ Use cases 🛠️**

- Static methods - **Validation or helper** functions.

**🛑 Worst practices 🛑**

- Instance methods
    - Using instance methods **when no instance data is needed.**
    - Modifying **attributes** that **should stay internal without validation**.
    - Writing **very large methods** that handle **unrelated logic**.
- Class methods
    - Using them when **instance data is required**.
    - Modifying **instance attributes from class methods**.
    - Overusing them when a static method would be clearer.
- Static methods
    - **Accessing instance or class attributes** from static methods.
    - Using them when the function **would be clearer as an instance or class method**.
    - Turning a class into a container of **unrelated utility functions**.

Sources:

### Alternative constructor

**🔽 What? 🔽**

- 

**🔁 What does it do? 🔁**

- 

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- powerful, elegant, and distinctively “Pythonic” solution to the problem of different types of objects that could be inserted in methods, or God methods problem
- to write a class that allows you to construct objects using arguments of **different data types**
- or even a **different number of arguments**

🤔 **How does it work?** 🤔

- Python does **not** support **constructor overloading**

**✍️ How to use it? ✍️**

- `@classmethod` decorator

**👍 Advantages 👍**

- 

**👎 Disadvantages 👎**

- 

**↔️ Alternatives ↔️**

- Another option is to employ the `@singledispatchmethod` decorator for method overloading based on argument types.

**✅ Best practices ✅**

- separate **parsing logic** from the main constructor
- useful for **data deserialization**
- encapsulate **standard configurations** inside the class

**🛠️ Use cases 🛠️**

- Parsing data received from files, APIs, or configuration **strings**
- Creating an object from a **dictionary** (common for APIs/JSON)
- Code Example
    
    ```python
    class User:
    
        def __init__(self, name, age):
            self.name = name
            self.age = age
    
        @classmethod
        def from_string(cls, data):
            name, age = data.split(",")
            return cls(name, int(age))
            
        @classmethod
        def from_dict(cls, data):
            return cls(data["name"], data["age"])
    
    user = User.from_string("Alice,30")
    print(user.name, user.age)
    data = {"name": "Leonard", "price": 12}
    product = User.from_dict(data)
    ```
    
- Creating predefined **configurations**
    
    ```python
    class ServerConfig:
    
        def __init__(self, host, port):
            self.host = host
            self.port = port
    
        @classmethod
        def development(cls):
            return cls("localhost", 8000)
    
        @classmethod
        def production(cls):
            return cls("0.0.0.0", 80)
    
    dev_server = ServerConfig.development()
    prod_server = ServerConfig.production()
    ```
    

**🛑 Worst practices 🛑**

- 

Sources:

## Encapsulation

**🔽 What? 🔽**

- is the idea and mechanism of **building** the data (**attributes**) and **methods** (functions) that **operate** on the data into single unit, called as an object.

**🔁 What does it do? 🔁**

- restricts direct access to some of an object’s components.
- **Data Hiding**: An object’s internal state is hidden from the **outside** world. This is also referred to as information hiding.
- **Access Restrictions**: External code cannot directly access the object’s internal state. Instead, it must use specific methods provided by the object (like **getters and setters**) to read or modify its state.
- **Simplification**: By interacting with an object through a well-defined interface, the **complexity** of the system is **reduced**, making it easier to understand and maintain.

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- 

🤔 **How does it work?** 🤔

- In Python there is not a real encapsulation and all data and methods are public in fact.

**✍️ How to use it? ✍️**

- 

**👍 Advantages 👍**

- 

**👎 Disadvantages 👎**

- 

**↔️ Alternatives ↔️**

- 

**✅ Best practices ✅**

- **Hide** internal data using `_protected` or `__private` attributes and **expose behavior through methods**.
- **Control access** with methods or properties (`@property`, `setters`) instead of direct attribute manipulation.
- **Validate** data **inside the class** to keep the object in a valid state.
- **Expose** only what is **necessary** (**minimal public interface**).
- Keep internal implementation **flexible** so it can change without breaking external code.
- **Abstraction** defines **what** an object can do, while **encapsulation** controls **how** its data is accessed.

**🛠️ Use cases 🛠️**

- 

**🛑 Worst practices 🛑**

- Accessing `_protected` or `__private` variables from external code.
- Manipulating mangled private attributes like `_ClassName__var` directly.
- Exposing internal data structures (e.g., returning a mutable list that external code can freely modify).
- Using public attributes for **critical state** without validation.
- Overusing **getters/setters** when direct public attributes would be simpler and clearer.

Sources:

### Internal or Protected Variables

**🔽 What? 🔽**

- 

**🔁 What does it do? 🔁**

- 

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- to signal developers, that this variables is used for internal usage, but not for the outside usage. Id does not prevent access.

🤔 **How does it work?** 🤔

- Python allows access to `_internal` variables from outside the class, but **developers agree they *shouldn’t* do it.**
- We can imagine a worker who is responsible for bringing papers from one floor to another. So we ask him to bring document from second floor called NDA of the company. But we don’t tell him that he need to go with the elevator or by his legs, should it be printed on the paper, or will he bring a CD with a Document. No, he knows his functions, and we do not tell him what to do with it.

**✍️ How to use it? ✍️**

- 

**👍 Advantages 👍**

- 

**👎 Disadvantages 👎**

- 

**↔️ Alternatives ↔️**

- Private variable

**✅ Best practices ✅**

- Use them only **inside the class and its subclasses**, not from outside.
- Prefix with a single underscore (_var) to signal **internal use** clearly.
- Access them through **getter/setter methods** if external interaction is needed.
- Use [Naming convention best practices](https://www.notion.so/Python-319745f820dc80a4a8aad0e7083b88dc?pvs=21)

**🛠️ Use cases 🛠️**

- Employee salary. Protecting salary with `_salary` means external code should not change it directly, because salary updates usually require rules or validation (taxes, raises, permissions, etc.).
    
    ```python
    class Employee:
        def __init__(self, salary):
            self._salary = salary  # protected
    
    class Manager(Employee):
        def give_bonus(self, amount):
            self._salary += amount   # subclass allowed to modify
    
    emp = Manager(1000)
    emp.give_bonus(500)
    print(emp._salary)   # works but external code SHOULD NOT do this
    ```
    

**🛑 Worst practices 🛑**

- Accessing `_protected` variables directly from external code of the class.
- Using them as a “**secret**” or assuming they are **truly private**.
- **Changing** them arbitrarily from **outside the class**, breaking encapsulation.
- **Mixing** underscore and public naming **inconsistently** (_data vs data).
- **Overusing** them instead of proper encapsulation with methods.

Sources:

### Private variables

**🔽 What? 🔽**

- 

**🔁 What does it do? 🔁**

- 

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- for name mangling to **prevent** accident usage of the property.
- It refers to **preventing name conflicts** in inheritance

🤔 **How does it work?** 🤔

- It changes the name from `__propery_name` to `_ClassName__property_name`.

**✍️ How to use it? ✍️**

- 

**👍 Advantages 👍**

- 

**👎 Disadvantages 👎**

- 

**↔️ Alternatives ↔️**

- 

**✅ Best practices ✅**

- Use double underscore (`__var`) for **critical** internal data that shouldn’t be **accidentally** overwritten, especially in **inheritance** scenarios.
- Access them only through methods like **getters/setters**, not directly.
- Use **descriptive** names so their purpose is clear (`__balance`, `__config`).
- Apply them when **subclass conflicts might occur**, since name mangling protects the original variable.

**🛠️ Use cases 🛠️**

- Balance in BankAccount setting only during initiating, without modificating this in the future. We cannot modificate a balance in the same instance.
    
    ```python
    class BankAccount:
        def __init__(self, owner, initial_balance=0):
            self.owner = owner
            self.__balance = initial_balance # The actual balance is "private"
    
        def deposit(self, amount):
            if amount > 0:
                self.__balance += amount
                print(f"Deposited ${amount}. New balance: ${self.__balance}")
    
        def withdraw(self, amount):
            if amount > 0 and amount <= self.__balance:
                self.__balance -= amount
                print(f"Withdrew ${amount}. Remaining balance: ${self.__balance}")
            else:
                print("Insufficient funds or invalid amount!")
    
        def get_balance(self):
            # A public method to safely retrieve the balance value
            return self.__balance
    
    # Usage
    account = BankAccount("Alice", 100)
    account.deposit(50)
    account.withdraw(25)
    # Attempting to modify the balance directly will raise an AttributeError
    try:
        account.__balance = 1000000 
    except AttributeError as e:
        print(f"\nError: {e}") 
    # The actual balance remains protected
    print(f"Current balance: ${account.get_balance()}")
    
    ```
    
- 

**🛑 Worst practices 🛑**

- Keep them limited to truly internal logic — **don’t overuse** for everything.

Sources:

## Inheritance

**🔽 What? 🔽**

- fundamental concept in object-oriented programming (OOP)

**🔁 What does it do? 🔁**

- allows developers to **create** a **new class** that is **based** on an **existing class**

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- to inherit **attributes and methods** from the **parent** or base **class**
- for cases where a class should **extend the functionality of another class**, *implying a strong relationship*.

🤔 **How does it work?** 🤔

- This mechanism enables the new class, often referred to as the **child or subclass**.
- is often explained through the “**is-a**” relationship, which is a way to establish a hierarchy between classes to indicate that **one class is a specialized version of another**. “Class B is a **type** of Class A”. The “is-a” relationship signifies that a subclass (or derived class) is a **more specific form** of the **superclass** (or base class) it inherits from. This means that objects of the **subclass** can be **treated as** objects of the **superclass**, although they may have **additional properties or behaviors**.

**✍️ How to use it? ✍️**

- Call parent implementations with `super()` when **extending functionality**.

**👍 Advantages 👍**

- code reuse
- establishing a **clear hierarchy**
- **facilitating the development** of complex software systems
- **maintenance** of complex software systems

**👎 Disadvantages 👎**

- May violate [LSP](https://www.notion.so/Python-319745f820dc80a4a8aad0e7083b88dc?pvs=21)

**↔️ Alternatives ↔️**

- Composition
- Mixins

**✅ Best practices ✅**

- Use inheritance only when there is a clear **“is-a”** relationship (e.g., Dog is an Animal).
- Keep the inheritance hierarchy simple and shallow, but not many multilevels.
- Use method overriding carefully and **respect the parent class’s behavior**.
- Prefer **composition** over inheritance when **reuse** is the only goal.

**🛠️ Use cases 🛠️**

- Modeling **real-world hierarchies** (Vehicle → Car, Truck).
- **Framework design** where users **extend base classes**.
- Polymorphism (different objects responding to the same method).

**🛑 Worst practices 🛑**

- Avoid inheritance if the relationship **does not fit the “is-a” model**. In such cases, consider using **composition or interfaces** to achieve the desired functionality.
- Using inheritance only to reuse code when there is **no logical relationship**.
- Creating **very deep** class **hierarchies** that are **hard to maintain**.
- Overriding methods and **breaking** the parent class **contract**.
- **Not** calling `super()` when the parent initialization is required.
- Making **base classes** too **complex** or too **tightly coupled**.
- awkward inheritance hierarchy where animals and vehicles share a common ancestor. Use mixins as alternative
    - UML diagram, where animal and vehicle share the same base class Serializer, because they have the same method in their children
        
        ![image.png](OOP/image.png)
        
- tendency for **overgeneralization.** When the base class becomes too broad in scope, subclasses start to inherit **unnecessary features**. For example, if a vehicle requires another serialization method, then all animals automatically inherit it, whether they need one or not

Sources:

### Abstraction

**🔽 What? 🔽**

- is a fundamental **concept** in OOP

**🔁 What does it do? 🔁**

- **hides** the **complexity** of a system by providing a **simpler interface**
- **Simplifying client interactions**: It offers a straightforward interface for clients (other pieces of code that use the class) to interact with class objects. Clients can call methods defined in the interface without needing to understand the intricate details of how the methods are implemented.
- **Hiding internal complexity**: Abstraction masks the complexity of internal class implementations **behind an interface**. This ensures that the client code does not have to deal with the inner workings of a class, thus promoting a decoupled and more maintainable codebase.

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- when we understand what type of methods will do subclasses but without specifications of this method
- **Abstraction** defines **what** an object can do, while **encapsulation** controls **how** its data is accessed.

🤔 **How does it work?** 🤔

- Basic example
    
    ```python
    from abc import ABC, abstractmethod
    
    class Vehicle(ABC):
    
    	@abstractmethod
    	def go(self):
    		pass
    	
    # vehicle = Vehicle() Would not create and initiate a new object, 
    # because this class is abstract and meant to be subclassed.
    
    class Car(Vehicle):
    	def go(self):
    		print("You drive the car")
    
    class Boat(Vehicle):
    	def go(self):
    		print("Your boat sails on the water")
    ```
    

**✍️ How to use it? ✍️**

- Abstract classes are meant to be **subclassed**. They may contain abstracts methods that are declared **but not implemented**.

**👍 Advantages 👍**

- Enhanced **modularity**: By encapsulating complex logic within classes and exposing only what **is necessary through interfaces**, code becomes more modular. This modularity facilitates easier code management and updates.
- **Scalability**
- Improved **code readability**: Abstraction makes the code more intuitive and easier to understand by highlighting the interactions over the implementations.
- Increased **maintainability**: Changes to the internal implementation of a class do not affect the client code, as long as the interface remains unchanged. This makes the system more resilient to changes and easier to maintain.
- Better **code reusability**: Abstracting common functionalities into interfaces allows for reusing code across different parts of a project or even across projects, reducing redundancy and effort.
- Code **Safety**. If we use abstract classes it gives all the meaningful instructions during the subclass addind to the code.

**👎 Disadvantages 👎**

- **Performance Considerations**: In some high-performance scenarios, the overhead of using abstract base classes might be a concern.
- **Design Overhead**: The need to thoroughly understand the base class design before extending it can increase the learning curve for new developers.

**↔️ Alternatives ↔️**

- 

**✅ Best practices ✅**

- Expose **clear and minimal public interfaces** (methods users actually need).
- Hide implementation details using private (__var) or protected (_var) members.
    
    ```python
    from abc import ABC, abstractmethod
    
    class Storage(ABC):
    
        def save(self, data):
            processed = self._prepare_data(data)   # hidden internal step
            self._write(processed)
    
        def _prepare_data(self, data):             # protected internal logic
            return data.strip().lower()
    
        @abstractmethod
        def _write(self, data):                    # subclasses must implement
            pass
    
    class FileStorage(Storage):
        def _write(self, data):
            print(f"Saving '{data}' to file")
    
    class DatabaseStorage(Storage):
        def _write(self, data):
            print(f"Saving '{data}' to database")
    
    s = FileStorage()
    s.save("  HELLO  ")
    ```
    
- Use abstract base classes when defining **required** behavior **for subclasses**.
- Keep abstractions simple and stable, even if the internal implementation changes.
- Design abstractions around **what** the object does, not **how** it does it.

**🛠️ Use cases 🛠️**

- **Framework** and library design
- Defining interfaces. Ensure subclasses implement **required behavior**
- Polymorhism. Swappable implementations. Different implementations follow the same interface.
- Complex system **simplification**. Hide complicated internal logic behind a simple API.

**🛑 Worst practices 🛑**

- Creating **too many abstraction layers** that make the code hard to follow.
- **Designing** abstractions **too early** before understanding the problem.
- **Exposing internal implementation** through the public API.
- Making abstract classes too **large or too complex**.
- Using abstraction where simple **functions or classes would be clearer**.

Sources:

### Multiple inheritance

**🔽 What? 🔽**

- 

**🔁 What does it do? 🔁**

- 

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- when a **class** naturally **combines** **behaviors** from **multiple sources**.

🤔 **How does it work?** 🤔

- 

**✍️ How to use it? ✍️**

- 

**👍 Advantages 👍**

- **Flexibility**: It offers more flexibility by allowing a class to inherit features from multiple classes.
- **Feature-rich**: Subclasses can be more feature-rich, incorporating attributes and methods from multiple superclasses.

**👎 Disadvantages 👎**

- **Complexity**: The hierarchy can become complex, making it harder to trace the source of methods and attributes.
- **Diamond Problem**: The diamond problem is a particular complication where an ambiguity arises in the inheritance hierarchy, specifically when a class inherits from two classes that both inherit from the same superclass.
- Increased Risk of **Method Collision**: With multiple inheritance, there’s a higher risk of method **name collision**, where different superclasses have methods with the same name but different functionalities. This can lead to **unexpected behaviors** if not carefully managed, as the subclass might inherit and execute the **wrong method version**, leading to bugs that are **hard to trace and fix**.
- **Design Challenges:** Good design often involves ensuring that objects have a **single, clear responsibility**. Multiple inheritance can blur these lines, leading to objects that are trying to do too much or that mix unrelated functionalities. This can violate the **Single Responsibility Principle, one of the SOLID** principles of object-oriented design, making classes **less cohesive and harder to understand**.

**↔️ Alternatives ↔️**

- **Composition** over Inheritance: Using composition, where an object contains instances of other objects to extend its functionality, can often be a more **flexible** and **less complex** way to achieve the same goals as multiple inheritance.
- **Interfaces or Mixins**: In languages that support them, interfaces or mixins can provide a way to share **methods across classes without** the **complexity of multiple inheritance**.

**✅ Best practices ✅**

- Use it when a **class** naturally **combines behaviors** from **multiple sources**.
- Prefer **small**, focused mixin classes that add one capability
- Use super() consistently so Python’s MRO (Method Resolution Order) works correctly.
- Keep **mixins stateless** or simple when possible.
- Document clearly which classes are intended to be mixins vs base classes.

**🛠️ Use cases 🛠️**

- **Mixins** adding features like **logging, serialization, or validation.**
- **Combining independent behaviors** (Flyable, Swimmable).
- Framework patterns where objects need **multiple capabilities**.

**🛑 Worst practices 🛑**

- Creating complex **diamond** inheritance structures without understanding MRO.
- **Mixing classes** that were **not** designed **for multiple inheritance**.
- Using multiple inheritance when **composition would be clearer**.
- Having **conflicting method names** across parent classes.
- Building **large hierarchies** where debugging method resolution becomes difficult.

Sources:

### Method Resolution Order

**🔽 What? 🔽**

- 

**🔁 What does it do? 🔁**

- refers to the **order** in which Python **looks for** a method in a **hierarchy of classes**.

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- Especially relevant in the context of **multiple inheritance**, where a class can inherit features from more than one parent class
- for determining how and where Python finds the methods you call

🤔 **How does it work?** 🤔

- **Linearization:** Python uses a strategy called **C3 Linearization** to flatten the class hierarchy in a specific order that ensures each class is encountered once before its parents and in the order specified in the class definition.
- **Left-to-Right, Depth-First:** The search for methods begins from the current class and proceeds to the parent classes, following a left-to-right, depth-first order. This means Python **first** looks at the **leftmost** parent class, **moving down** its hierarchy (depth-first), before proceeding to the next parent class.

**✍️ How to use it? ✍️**

- `super()` Function: The `super()` function in Python leverages MRO to determine which method or attribute to invoke, making it easier to use inheritance effectively, especially in complex class hierarchies.
- You can view the MRO of a class by using the `__mro__` attribute or the `mro()` method. `print(Child.__mro__)`  will show the order in which Python looks for methods and attributes, helping to resolve ambiguities in multiple inheritance scenarios.

### Mixin

**🔽 What? 🔽**

- tool
- Mixin class is a class
- conventional pattern

**🔁 What does it do? 🔁**

- has methods that other classes can use

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- reuse code across multiple Python classes **without forcing** them into a **rigid inheritance hierarchy**
- when **multiple classes** **need the same capability**

🤔 **How does it work?** 🤔

- We are mixing new method in the subclass, which needs them to use.
- rely on **multiple inheritance** to combine features from different classes

**✍️ How to use it? ✍️**

- **inherit** it together with the main classes
- **no syntactical difference** between standard classes and mixin classes—the distinction is purely semantic
- You create mixins by defining classes with **specific behaviors** that other classes can inherit **without forming an is-a relationship**
- **Naming convention**: That’s the most obvious giveaway. While not mandatory, it’s considered Pythonic to include a **distinctive suffix (**`Mixin`**)** in the class name. This clearly communicates the special purpose of your class and its intended use since Python has no dedicated syntax for mixins. Additionally, its name should reflect the feature provided by the mixin, like the ability to serialize an object.
- **Plain class**: Because mixins are meant to provide isolated, reusable features—rather than to enforce an inheritance structure—they typically **don’t have any parent classes**. This minimizes their scope and reduces the likelihood of incorrect name resolution in multiple inheritance scenarios.
- **Single behavior**: A mixin class has just one responsibility, making it reusable and composable with other mixins—as long as those mixins provide orthogonal or non-overlapping features. Note that this **doesn’t** **necessarily mean** that your **mixin** must **only** define a **single method**.
- **Statelessness**: Mixins **rarely define constructors or instance attributes** of their own, making them safe to integrate with other classes through multiple inheritance without conflicts. The behavior encapsulated by a mixin class depends solely on an external state. Mixins **often rely on attributes of the classes they’re mixed into**.
- Non-standalone: Mixins are designed to augment other classes with new or modified behaviors. They typically **don’t make any sense independentl**y, so you almost never instantiate mixin classes directly.

**👍 Advantages 👍**

- reuse code
- Modularity
- Flexibility

**👎 Disadvantages 👎**

- 

**↔️ Alternatives ↔️**

- Functions for simple reusable logic
- Decorators when behavior must wrap or intercept execution

**✅ Best practices ✅**

- How Can You Use Stateful Mixins Safely?
    - Stateful mixins require careful design to manage instance attributes and avoid conflicts with other classes.
    - Move the State to Class Attributes. You can **minimize the hurdles of multiple inheritance** by taking a different route. Simply **eliminate** the **initializer methods** and **replace instance attributes with class attributes**.
        
        ```python
        class TypedKeyMixin:
            key_type = object
        
            def __setitem__(self, key, value):
                if not isinstance(key, self.key_type):
                    raise TypeError(
                        f"key must be {self.key_type} but was {type(key)}"
                    )
                super().__setitem__(key, value)
        
        class TypedValueMixin:
            value_type = object
        
            def __setitem__(self, key, value):
                if not isinstance(value, self.value_type):
                    raise TypeError(
                        f"value must be {self.value_type} but was {type(value)}"
                    )
                super().__setitem__(key, value)
        ```
        
        ```python
        >>> from collections import UserDict
        >>> from stateful_v1 import TypedKeyMixin, TypedValueMixin
        
        >>> class Inventory(TypedKeyMixin, TypedValueMixin, UserDict):
        ...     key_type = str
        ...     value_type = int
        ...
        
        >>> fruits = Inventory()
        
        >>> fruits["apples"] = 42
        
        >>> fruits["🍌".encode("utf-8")] = 15
        Traceback (most recent call last):
          ...
        TypeError: key must be <class 'str'> but was <class 'bytes'>
        
        >>> fruits["bananas"] = 3.5
        Traceback (most recent call last):
          ...
        TypeError: value must be <class 'int'> but was <class 'float'>
        
        >>> vars(fruits)
        {'data': {'apples': 42}}
        ```
        
    - [Hide the State in Function Closures](https://realpython.com/python-mixin/#hide-the-state-in-function-closures). Use functions that defines a class _ which will be returned.
    - [Compose Behaviors With Decorators](https://realpython.com/python-mixin/#compose-behaviors-with-decorators)
- Documenting with PEP 257 and PEP 8
    
    docstring should include: 
    
    - that it is a mixin
    - its purpose
    - that it should be used via inheritance
    
    ```python
    class LoggingMixin:
        """
        Mixin that adds logging capability.
    
        This class is intended to be used with multiple inheritance.
        It should not be instantiated directly.
        """
    
        def log(self, message):
            print(f"[LOG]: {message}")
    ```
    
    ```python
    class User(LoggingMixin):
        """Application user that supports logging via LoggingMixin."""
        pass
    ```
    

**🛠️ Use cases 🛠️**

- Basic example. This class defines one method, which returns a dictionary representation of an object, handling two cases. If the object uses `.__slots__`, then `.serialize()` builds a dictionary using a comprehension expression. Otherwise, the method returns an object’s `.__dict__` attribute by calling `vars()` on it.
    
    ```python
    class SerializableMixin:
        def serialize(self) -> dict:
            if hasattr(self, "__slots__"):
                return {
                    name: getattr(self, name)
                    for name in self.__slots__
                }
            else:
                return vars(self)
    ```
    
- Mixin Implementation. Conceptually, `AppSettings` is a more **specialized type** of `SimpleNamespace` with an **additional capability** to serialize itself to JSON. The `JSONSerializableMixin` has no knowledge of `AppSettings`, `User`, or any other descendant type that you may potentially plug it into.
    
    ```python
    import json
    from typing import Self
    
    class JSONSerializableMixin:
    		@classmethod
        def from_json(cls, json_string: str) -> Self:
            return cls(**json.loads(json_string))
    
        def as_json(self) -> str:
            return json.dumps(vars(self))
    
    # Single inheritance:
    class User(JSONSerializableMixin):
        pass
    # Multiple inheritance:
    class AppSettings(JSONSerializableMixin, SimpleNamespace):
    		def save(self, filepath: str | Path) -> None:
    				Path(filepath).write_text(self.as_json(), encoding="utf-8")
    
    ```
    

**🛑 Worst practices 🛑**

- Going Overboard With Mixins. Spotting so many mixins in one place is a good indicator of a **God object** with too **many responsibilities** that would be better off refactored. For instance, you might decouple it by grouping related functionalities that are frequently used together into higher-level classes. Including more than a few mixins at a time increases your code’s **complexity,** making it **harder to understand** and **debug**.
- **Ordering Mixins Incorrectly.**  Violates MRO mistakes.
    - Placing Mixins **After Base Classes**. only **exception** to this rule is when a mixin provides unique methods that are **guaranteed** not to conflict with those of other classes
- Defining Uncooperative Constructors. **Don’t include** an `.__init__()` method in your **mixin** classes unless you have a compelling reason and understand the possible outcomes.
- Using Conflicting Instance Attributes

Sources:

[What Are Mixin Classes in Python? – Real Python](https://realpython.com/python-mixin/)

## Polymorphism

April 6, 2026 [Знати GRASP](https://www.notion.so/GRASP-331745f820dc8056980bd3c80b4d8be6?pvs=21) 

**🔽 What? 🔽**

- a core concept in OOP
- GRASP principle

**🔁 What does it do? 🔁**

- refers to the **ability** of a single interface to **support** entities of **multiple types**
- or the **ability** of different **objects** to **respond in a unique way** to the same **method call**.

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- 

🤔 **How does it work?** 🤔

- polymorphism is **inherent** in its design, allowing for **flexible and dynamic use** of objects.

**✍️ How to use it? ✍️**

- Basic example
    
    ```python
    # Integer addition
    result = 1 + 2
    print(result)  # Output: 3
    
    # String concatenation
    result = "Data" + "Science"
    print(result)  # Output: DataScience
    ```
    
- Example in OOP
    
    ```python
    class Dog:
        def speak(self):
            return "Woof!"
            
    class Cat:
        def speak(self):
            return "Meow!"
            
    def animal_sound(animal):
        print(animal.speak())
    # Polymorphism in action
    dog = Dog()
    cat = Cat()
    animal_sound(dog)  # Output: Woof!
    animal_sound(cat)  # Output: Meow!
    ```
    

**👍 Advantages 👍**

- Data scientists can design their codebase to be more **abstract and versatile**, facilitating **easier experimentation and iteration** across diverse data science tasks.

**👎 Disadvantages 👎**

- 

**↔️ Alternatives ↔️**

- 

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- 

**🛑 Worst practices 🛑**

- 

Sources:

by Types:

### Duck typing

**🔽 What? 🔽**

- A Python phlosophy

**🔁 What does it do? 🔁**

- says that **type** or class of the object is **less important** than methods it defines.

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- 

🤔 **How does it work?** 🤔

> “If it looks like a duck and quacks like a duck, it must be a duck.”
> 

**✍️ How to use it? ✍️**

- 

**👍 Advantages 👍**

- 

**👎 Disadvantages 👎**

- 

**↔️ Alternatives ↔️**

- 

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- 

**🛑 Worst practices 🛑**

- 

Sources:

### Method overloading

**🔽 What? 🔽**

- 

**🔁 What does it do? 🔁**

- refers to the ability to ****have **multiple methods** with the **same name** but **different parameters**

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- to provide different implementations for a method, depending on the **number** and **type** of **arguments** passed

🤔 **How does it work?** 🤔

- Python handles this concept differently due to its nature and how it handles function definitions. In Python, methods are defined in a **class**, and their **behavior** does **not change** based on the **number or types** of arguments passed. If you **define multiple methods** with the same name but **different parameters** in the same **scope**, the **last definition will overwrite the previous ones**.
- Python relies on its **dynamic typing** and other features to achieve similar functionality

**✍️ How to use it? ✍️**

- Basic example without multiple dispatcher decorator
    
    ```python
    class Example:
        def greet(self, name):
            print(f"Hello, {name}")
    def greet(self):  # This will override the previous 'greet'
        print("Hello")
    # Create an instance
    example = Example()
    example.greet()  # Outputs: Hello
    # example.greet("Python")  
    # This would raise an error because the greet method with one 
    # argument has been overridden
    ```
    

**👍 Advantages 👍**

- 

**👎 Disadvantages 👎**

- 

**↔️ Alternatives ↔️**

- 

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- 

**🛑 Worst practices 🛑**

- 

Sources:

## Composition

**🔽 What? 🔽**

- is a fundamental concept in OOP.

**🔁 What does it do? 🔁**

- involves constructing complex objects by **including objects** of **other classes** within them, known as **components**

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- for designing robust and adaptable software systems
- more **flexible** and **loosely coupled** designs compared to traditional **inheritance-based** approaches
- is ideal for cases where a **class** simply **needs** to utilize **functionalities** of **other classes without extending them**, indicating a weaker relationship

🤔 **How does it work?** 🤔

- models a **“has-a”** relationship between classes
- allows a composite class to utilize the functionalities of its component classes, without inheriting from them directly. Essentially, the composite class “has a” **component (or many components)** of another class.
- **instead of rewriting code**, a **class** can simply **include objects** of existing classes to use their functionality.

**✍️ How to use it? ✍️**

- In example, in the software system of the **school**, we have classes representing `Teachers` and `Departments`. Instead of using inheritance, which would imply a `teacher` "is a" `department`, we use composition to model a more realistic **"has a"** relationship, where a department **"has"** teachers.
    
    ```python
    class Teacher:
        def __init__(self, name, subject):
            self.name = name
            self.subject = subject
        
        def **get_details(self)**:
            return f"{self.name} teaches {self.subject}."
            
    class Department:
        def __init__(self, name):
            self.name = name
            self.teachers = **[]  # Composition happens here**
    
        def add_teacher(self, teacher):
            self.teachers.append(teacher)
        
        def get_department_details(self):
            details = f"Department: {self.name}\n"
            details += "Teachers:\n"
            for teacher in self.teachers:
                details += f"- {teacher.**get_details()**}\n"
            return details     
    
    # Creating teacher instances
    teacher1 = Teacher("Alice Smith", "Mathematics")
    teacher2 = Teacher("Bob Johnson", "Science")
    
    # Creating a department and adding teachers to it
    math_science_department = Department("Math & Science")
    math_science_department.add_teacher(teacher1)
    math_science_department.add_teacher(teacher2)
    
    # Displaying department details
    print(math_science_department.get_department_details())
    ```
    
- Media player (Composition + Abtraction).
    
    ```python
    from abc import ABC, abstractmethod
    
    class MediaFile(ABC):
        def __init__(self, name):
            self.name = name
    
        @abstractmethod
        def play(self):
            pass
            
    class AudioFile(MediaFile):
        def play(self):
            return f"Playing audio file: {self.name}"
    
    class VideoFile(MediaFile):
        def play(self):
            return f"Playing video file: {self.name}"
    
    class MediaPlayer:
        def __init__(self):
            self.playlist = []
    
        def add_media(self, media_file: MediaFile):
            self.playlist.append(media_file)
    
        def play_all(self):
            for media in self.playlist:
                print(media.play())
                
    # Creating instances of media files
    audio1 = AudioFile("song1.mp3")
    video1 = VideoFile("video1.mp4")
    
    # Creating the media player
    player = MediaPlayer()
    
    # Adding media files to the player's playlist
    player.add_media(audio1)
    player.add_media(video1)
    
    # Playing all media in the playlist
    player.play_all()
    ```
    
- Project management system
    
    ```python
    from abc import ABC, abstractmethod
    
    class ProjectTask(ABC):
        """Represents a task within a data science project."""
    
        @abstractmethod
        def get_effort_estimate(self) -> float:
            """Returns the effort estimate to complete the task."""   
    
    class DataCollectionTask(ProjectTask):
        """Task related to data collection efforts."""
    
        def __init__(self, data_sources: int):
            self.data_sources = data_sources
    
        def get_effort_estimate(self) -> float:
            return 2.0 * self.data_sources
    
    class AnalysisTask(ProjectTask):
        """Task for data analysis."""
    
        def __init__(self, complexity_level: int):
            self.complexity_level = complexity_level
    
        def get_effort_estimate(self) -> float:
            return 5.0 * self.complexity_level
    
    class ModelingTask(ProjectTask):
        """Machine Learning modeling task."""
    
        def __init__(self, number_of_models: int):
            self.number_of_models = number_of_models
    
        def get_effort_estimate(self) -> float:
            return 10.0 * self.number_of_models
    
    from typing import Optional, List
    
    class DataScienceEmployee:
        """Represents an employee working on data science projects."""
    
        def __init__(self, name: str, id: int, project_tasks: List[ProjectTask], base_salary: float, bonus: Optional[float] = None):
            self.name = name
            self.id = id
            self.project_tasks = project_tasks
            self.base_salary = base_salary
            self.bonus = bonus
    
        def compute_compensation(self) -> float:
            total_effort = sum(task.get_effort_estimate() for task in self.project_tasks)
            compensation = self.base_salary
            if self.bonus is not None:
                compensation += self.bonus * total_effort
            return compensation  
    
    def main():
        """Demonstrate the data science project management system."""
    
        alice_tasks = [DataCollectionTask(data_sources=5), AnalysisTask(complexity_level=3)]
        alice = DataScienceEmployee(name="Alice", id=101, project_tasks=alice_tasks, base_salary=70000, bonus=150)
    
        bob_tasks = [ModelingTask(number_of_models=2)]
        bob = DataScienceEmployee(name="Bob", id=102, project_tasks=bob_tasks, base_salary=85000, bonus=300)
    
        print(f"{alice.name} has tasks with a total effort estimate of {sum(task.get_effort_estimate() for task in alice_tasks)} and total compensation of ${alice.compute_compensation()}.")
        print(f"{bob.name} has tasks with a total effort estimate of {sum(task.get_effort_estimate() for task in bob_tasks)} and total compensation of ${bob.compute_compensation()}.")
    
    if __name__ == "__main__":
        main()      
    ```
    

**👍 Advantages 👍**

- **Reusability**: Composition fosters **reusability** by allowing the **composite class** to leverage the implementation of its **components**.
- **Loose Coupling**: The relationship between the **composite** and **component** classes in composition is characterized by loose coupling. This implies that changes in the component class have minimal impact on the composite class, enhancing the system’s maintainability and flexibility.
- Modularity Enhance
- **Ease of Change**: Due to the loose coupling, software systems designed with composition are easier to modify and extend. New functionalities can be introduced or existing ones modified with little to no effect on the other parts of the system.
- **Flexibility** over Inheritance: While inheritance establishes a rigid “is-a” relationship, composition provides a more flexible “has-a” framework. This flexibility often makes composition a preferable choice in situations where software requirements are likely to evolve over time.
- **Avoids** class hierarchy **complexity**: Inheritance can lead to a deep and complicated class hierarchy that might become difficult to navigate and manage. Composition sidesteps this by encouraging simpler and flatter structure.

**👎 Disadvantages 👎**

- 

**↔️ Alternatives ↔️**

- Inheritance

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- When you need **dynamic behaviors**: If your application needs to alter its behavior at runtime, composition allows you to easily replace components **without restructuring the entire system**.
- When components can be used **across multiple contexts**: If the same functionality is needed in disparate parts of the application, composition allows you to **reuse** a component in various contexts without inheriting from it.
- To **avoid** the **diamond problem** in inheritance: This is a common issue in languages supporting multiple inheritance, where a class inherits from two classes, both of which inherit from a common base class. Composition eliminates this by allowing controlled and clear component use.
- When you want to **encapsulate** a complex structure: Composition can simplify the management of complex systems by **breaking down** functionality **into smaller, manageable parts** that are easier to understand and use.

**🛑 Worst practices 🛑**

- 

Sources:

[Composition vs Inheritance in Python OOP](https://medium.com/data-bistrot/composition-vs-inheritance-in-python-oop-d4b3c3d8b463)

# Design Patterns

**🔽 What? 🔽**

- general, reusable **solutions** to **common problems** that arise during the design and **development of software**.
- are **communicating objects and classes** that are customized to solve a general design problem in a particular context.
- isn't a complete design that can be written in code right away
- is a description or model for problem-solving that may be applied in a variety of contexts.

**🔁 What does it do? 🔁**

- **Creational design** **patterns** facilitate flexible object creation and code reuse. They deal with the process of **object creation**, trying to make it more flexible and efficient. It makes the system **independent** and how its objects are **created, composed, and represented.**
    - **Factory Method** provides an interface for **creating objects in superclass**, but subclasses are **responsible to create the instance of the class**.
    - **Abstract Factory Method** provides an interface for creating **families** of related or **dependent** objects **without specifying their concrete classes**.
    - **Builder Method** provides an interface for constructing an object and then have concrete builder classes that implement this interface to create specific objects in a **stepwise manner**.
    - **Prototype** Method. Creates new objects **by copying an existing object**, avoiding the overhead of creating objects from scratch.
    - **Singleton** Method. Ensures that a class has only **one instance** and provides a **global point** of access to that instance.
- **Structural** Patterns: **Assembling** objects and classes into **larger structures** while retaining their adaptability and efficiency.
    - **Adapter** Pattern: Converts the interface of a class **into another interface** that clients expect, enabling classes with incompatible interfaces to work together.
    - **Bridge** Pattern: **Decouples** an abstraction from its implementation, allowing both to evolve independently.
    - **Composite** Pattern: Composes objects into **tree structures** to represent **part-whole hierarchies**, making it easier to work with individual objects and compositions.
    - **Decorator** Pattern: Dynamically **adds responsibilities to objects**, providing a flexible alternative to subclassing for extending functionality.
    - **Facade** Pattern: Provides a simplified **interface** to a **complex subsystem**, making it easier to use and understand.
    - **Flyweight** Pattern: Shares instances of objects to support **large numbers** of fine-grained objects efficiently.
    - **Proxy** Pattern: provide a **substitute** or placeholder for another object to **control access** to the original object.
- **Behavioral Patterns**: Efficient **interaction** and allocation of responsibilities between objects, ensuring **effective communication**.
    - **Chain of Responsibility** Pattern: Creates a **chain of objects** that can handle requests, **avoiding coupling** the sender with its receivers.
    - **Command** Pattern: Turns a request into a stand-alone object, allowing parameterization of clients with different requests.
    - **Interpreter** Pattern: Defines a grammar for a language and an interpreter to interpret sentences in the language.
    - **Iterator** Pattern: Provides a way to access elements of a collection without exposing its underlying representation.
    - **Mediator** Pattern: Defines an object that centralizes communication between multiple objects, reducing direct dependencies between them.
    - **Memento** Pattern: Captures and restores an object’s internal state, allowing it to be restored to a previous state.
    - **Observer** Pattern: Defines a dependency between objects, ensuring that when one object changes state, all its dependents are notified and updated automatically.
    - **State** Pattern: Allows an object to change its behavior when its internal state changes, enabling cleaner, more maintainable conditional logic.
    - **Strategy** Pattern: Defines a family of algorithms, encapsulates each one and makes them interchangeable. Clients can choose an algorithm from this family without modifying their code.
    - **Template** Method Pattern: Defines the structure of an algorithm in a superclass but lets subclasses override specific steps of the algorithm.
    - **Visitor** Pattern: Separates an algorithm from an object structure, allowing new operations to be added without modifying the objects themselves.

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- useful for OOP
- Design patterns **enhance well-structured code**, but they can’t rescue fundamentally flawed designs. Fixing underlying issues precedes applying design patterns.
- Visualization
    
    ![image.png](OOP/image%201.png)
    

🤔 **How does it work?** 🤔

- Selecting an appropriate design pattern demands a deep understanding of both the **problem domain** and the **pattern’s principles**.

**✍️ How to use it? ✍️**

- 

**👍 Advantages 👍**

- Design patterns present **reusable strategies** for system structure, while algorithms outline a **precise sequence of actions** to achieve a particular objective.
- **Reusability**: Design patterns provide solutions that have already been **refined and tested**, enabling developers to reuse **successful strategies** for various projects.
- **Maintainability**: Applying design patterns promotes **modular and organized code**, making it easier to update and maintain in the long run.
- **Scalability**: Design patterns allow software systems to **evolve gracefully**, accommodating changes without causing widespread disruptions.
- **Consistency**: Using design patterns establishes a **common vocabulary and approach for developers**, fostering clear communication and collaboration.
- **Efficiency**: Design patterns address common challenges efficiently, **reducing development time and the potential for errors**.

**👎 Disadvantages 👎**

- 

**↔️ Alternatives ↔️**

- **Algorithms.** While algorithms and design patterns both **offer solutions for recurring problems**, their difference lies in their purpose:
    - **Algorithms** give a step-by-step solution to perform a specific task, often focusing on **solving computational problems**.
    - **Design Patterns**, however, give general guidelines or **blueprints** on how to **organize software** to **address repeated design problems**. Patterns are more concerned with the architecture and object interactions, whereas algorithms are concerned with an exact computational step.

**✅ Best practices ✅**

- Strive for natural alignment; forcing a pattern where it doesn’t fit can lead to future complications.
- Long-term consequences should also be weighed, as a quick solution might not translate well into scalability or maintenance.

**🛠️ Use cases 🛠️**

- 

**🛑 Worst practices 🛑**

- Another misconception views design patterns as **rigid templates to be followed blindly**. While patterns offer guidance, adaptability is key. Flexibility in pattern application ensures alignment with specific project needs. Patterns are **tools, not mandates**, and their usage should be pragmatic and attuned to the project’s unique goals.
- **Over-Engineering**: Avoid using design patterns unnecessarily, especially for **small or simple problems**. Over-engineering can lead to unnecessary complexity and overhead, making the codebase harder to understand and maintain.
- **Premature Optimization**: Avoid using design patterns solely for the sake of optimization **before performance issues are identified**. Premature optimization can lead to added complexity without significant benefits and can hinder future changes.
- **Unfamiliarity**: Avoid using design patterns if you or your team are **unfamiliar with them** or if their application does not align with the problem at hand. Using patterns incorrectly can lead to misuse and potential design flaws.
- **Project Constraints**: Consider project constraints such as **time, budget, and team expertise**. If applying a design pattern significantly increases development time or introduces unnecessary complexity, it may not be appropriate for the project.
- **Changing Requirements**: Be cautious when applying design patterns in **highly dynamic environments** where **requirements frequently change**. Overly rigid designs based on patterns may struggle to adapt to evolving requirements.

Sources:

[Design Patterns Cheat Sheet - When to Use Which Design Pattern? - GeeksforGeeks](https://www.geeksforgeeks.org/system-design/design-patterns-cheat-sheet-when-to-use-which-design-pattern/)

[Design Patterns in Python](https://python.plainenglish.io/design-patterns-in-python-f78682c6afe8/)

https://github.com/AmirLavasani/python-design-patterns/

[Design Patterns in Python](https://python.plainenglish.io/design-patterns-in-python-f78682c6afe8/)

[GitHub - faif/python-patterns: A collection of design patterns/idioms in Python](https://github.com/faif/python-patterns?tab=readme-ov-file)

[Python Design Patterns Tutorial - GeeksforGeeks](https://www.geeksforgeeks.org/python/python-design-patterns/)

[Software design pattern](https://en.wikipedia.org/wiki/Software_design_pattern)

[Design Patterns in Python](https://refactoring.guru/design-patterns/python)

[Any good resource on design patterns with examples in Python?](https://www.reddit.com/r/learnpython/comments/18eaakp/any_good_resource_on_design_patterns_with/)

[Design Patterns in Python: A Series](https://medium.com/@amirm.lavasani/design-patterns-in-python-a-series-f502b7804ae5)

## Creational Design Patterns

**🔽 What? 🔽**

- 

**🔁 What does it do? 🔁**

- 

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- when **object creation is complex**, involves **multiple steps**, or **requires specific initialization**.
- They're useful for promoting **reusability, encapsulating creation logic**, and **decoupling client code** from **classes** it instantiates.
- Creational patterns enhance **flexibility**, making it **easier to change** or **extend** object creation methods at runtime.
- to improve **maintainability, readability, and scalability** of your codebase.

🤔 **How does it work?** 🤔

- 

**✍️ How to use it? ✍️**

- 

**👍 Advantages 👍**

- 

**👎 Disadvantages 👎**

- 

**↔️ Alternatives ↔️**

- 

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- 

**🛑 Worst practices 🛑**

- 

Sources:

[Design Patterns Cheat Sheet - When to Use Which Design Pattern? - GeeksforGeeks](https://www.geeksforgeeks.org/system-design/design-patterns-cheat-sheet-when-to-use-which-design-pattern/)

### **Abstract Factory**

**🔽 What? 🔽**

- creational design pattern

**🔁 What does it do? 🔁**

- 

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- Use the Abstract Factory when your code needs to work with **various families** of **related products**, but you don’t want it to **depend on the concrete classes** of those **products**—they might be unknown beforehand or you simply want to allow for **future extensibility**.
- Consider implementing the Abstract Factory when you have a class with a **set of Factory Methods** that **blur its primary responsibility**.

🤔 **How does it work?** 🤔

- defines an interface for creating all distinct products but **leaves the actual product creation to concrete factory classes**. Each **factory type** corresponds to a **certain product variety**.
- The client code calls the **creation methods of a factory** object instead of creating products directly with a **constructor call** (`new` operator). Since a **factory** corresponds to a **single product variant**, all its products will be compatible.
- Client code works with factories and products only through their abstract interfaces. This lets the client code work with any product variants, created by the factory object. You just create a new concrete factory class and pass it to the client code.

- Abstract Factory can serve as **an alternative to Facade** when you only want to **hide the way** the **subsystem objects** are **created from the client code**.
- 

- You can use **Abstract Factory** along with **Bridge**. This pairing is useful when some abstractions defined by Bridge can **only work with specific implementations**. In this case, Abstract Factory can encapsulate these relations and **hide the complexity** from the client code.

**✍️ How to use it? ✍️**

- **Abstract Factory** classes are often based on a **set of Factory Methods**, but you can also use **Prototype** to compose the methods on these classes.
- How to implement:
    1. **Map out a matrix** of distinct **product types** versus **variants** of these products.
    2. Declare **abstract product interfaces for all product types**. Then make all concrete product classes **implement these interfaces**.
    3. Declare the abstract factory interface with a **set of creation methods for all abstract products**.
    4. Implement a **set of concrete factory classes**, one for each product variant.
    5. Create **factory initialization code** somewhere in the app. It should instantiate one of the concrete factory classes, depending on the application configuration or the current environment. Pass this factory object to all classes that construct products.
    6. Scan through the code and **find all direct calls to product constructors**. Replace them with **calls to the appropriate creation method on the factory object**.

**👍 Advantages 👍**

- You can be sure that the products you’re getting from a factory are **compatible with each other**.
- You **avoid tight coupling** between concrete products and client code.
- **Single Responsibility Principle**. You can extract the product creation code into **one place**, making the code easier to support.
- **Open/Closed Principle**. You can introduce new variants of products without breaking existing client code.

**👎 Disadvantages 👎**

- The code may become **more complicated than it should be**, since a lot of new interfaces and classes are introduced along with the pattern.

**↔️ Alternatives ↔️**

- 

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- The same UI elements in a cross-platform application are expected to behave similarly, but look a little bit different under different operating systems. Moreover, it’s your job to make sure that the UI elements match the style of the current operating system. You wouldn’t want your program to render macOS controls when it’s executed in Windows.
    
    ![example-1.5x.png](OOP/example-1.5x.png)
    
- 

**🛑 Worst practices 🛑**

- 

Sources:

[Abstract Factory](https://refactoring.guru/design-patterns/abstract-factory)

### Factory Method

**🔽 What? 🔽**

- is a **creational** design pattern that provides an interface for creating objects in a **superclass**, but **allows** subclasses to **alter the type** of objects that will be created.

**🔁 What does it do? 🔁**

- 

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- Use the Factory Method when you **don’t know** beforehand the **exact types and dependencies of the objects** your code should work with.

🤔 **How does it work?** 🤔

- 

- You can use **Factory Method** along with Iterator to **let collection subclasses** return **different types of iterators** that are compatible with the collections.

**✍️ How to use it? ✍️**

- The cross-platform dialog example.
    
    The base `Dialog` class uses different UI elements to render its window. Under various operating systems, these elements may look a little bit different, but they should still behave consistently. A button in Windows is still a button in Linux.
    
    ![example-1.5x.png](OOP/example-1.5x%201.png)
    
- Many designs start by using **Factory Method** (less complicated and more customizable via subclasses) and evolve toward **Abstract Factory, Prototype, or Builder** (more flexible, but more complicated).
- **How to Implement**
    1. Make all products follow the **same interface**. This interface should declare methods that **make sense in every product**.
    2. Add an **empty factory method** inside the **creator class**. The return type of the method should match the **common product interface**.
    3. In the creator’s code find all references to product constructors. One by one, replace them with calls **to the factory method**, while extracting the product creation code into the factory method. You might need to add a temporary parameter to the factory method to control the type of returned product. At this point, the code of the factory method may look pretty ugly. It may have a large `switch` statement that picks which product class to instantiate. 
    4. Now, create a **set of creator subclasses** for each **type of product** listed **in the factory method**. **Override** the factory **method** in the subclasses and extract the appropriate bits of construction code from the base method.
    5. If there are **too many product types** and it doesn’t make sense to create subclasses for all of them, you can **reuse the control parameter** from the base class in subclasses. For instance, imagine that you have the following hierarchy of classes: the base `Mail` class with a couple of subclasses: `AirMail` and `GroundMail`; the `Transport` classes are `Plane`, `Truck` and `Train`. While the `AirMail` class only uses `Plane` objects, `GroundMail` may work with both `Truck` and `Train` objects. You can create a new subclass (say `TrainMail`) to handle both cases, but there’s another option. The client code can pass an argument to the factory method of the `GroundMail` class to control which product it wants to receive.
    6. If, after all of the extractions, the **base factory method has become empty**, you can make it **abstract**. If there’s something left, you can make it a default behavior of the method.

**👍 Advantages 👍**

- You **avoid tight coupling** between the **creator and the concrete products.**
- **Single Responsibility Principle**. You can move the product creation code into **one place** in the program, making the code easier to support.
- **Open/Closed Principle**. You can introduce new types of products into the program without breaking existing client code.

**👎 Disadvantages 👎**

- The code may become more complicated since you need to introduce a **lot of new subclasses** to implement the pattern. The best case scenario is when you’re **introducing** the pattern into an **existing hierarchy of creator classes**.

**↔️ Alternatives ↔️**

- 

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- 

**🛑 Worst practices 🛑**

- 

Sources:

[Factory Method](https://refactoring.guru/design-patterns/factory-method)

### Builder

**🔽 What? 🔽**

- is a creational design pattern that lets you construct complex objects **step by step**.

**🔁 What does it do? 🔁**

- allows you to produce **different types and representations** of an object using the **same construction code**.

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- Use the Builder pattern to get rid of a “**telescoping constructor**”. It is a constructor which obtains **too many parameters**.
- when you want your code to be able to create **different representations** of some product (for example, stone and wooden houses).
- to construct **Composite trees** or other complex objects.

🤔 **How does it work?** 🤔

- Builder Mental Explanaiton.
    
    You might make the program too complex by creating a subclass for every possible configuration of an object.
    
    ![image.png](OOP/image%202.png)
    
- The pattern organizes object construction into a set of steps (`buildWalls`, `buildDoor`, etc.). To create an object, you execute a **series of these steps** on a builder object. The important part is that you **don’t need to call all of the steps**. You can call **only those steps** that are **necessary for producing** a particular configuration of an object. Some of the construction steps might require different implementation when you need to build various representations of the product. For example, walls of a cabin may be built of wood, but the castle walls must be built with stone. In this case, you can create several **different builder classes** that implement the same set of building steps, but in a **different manner**. Then you can use these builders in the construction process (i.e., an ordered set of calls to the building steps) to produce different kinds of objects.
- **Director**. You can go further and extract a **series of calls** **to the builder** steps you use to construct a product into a **separate class** called ***director***. The director class defines the **order** in which to **execute the building steps**, while the **builder** provides the **implementation for those steps**.

- You can combine Builder with **Bridge**: the director class plays the role of the **abstraction**, while different **builders** act as **implementations**.
- 

- You can use **Builder** when creating complex **Composite** trees because you can program its **construction steps** to **work recursively**.

**✍️ How to use it? ✍️**

- How to implement:
    1. Make sure that you can clearly define the common **construction steps** for building all available product representations. Otherwise, you won’t be able to proceed with implementing the pattern.
    2. Declare these steps in the **base builder interface**.
    3. Create a **concrete builder class** for each of the product representations and implement their construction steps.
        
        Don’t forget about implementing a **method for fetching the result of the construction**. The reason why this method can’t be declared inside the builder interface is that various builders may construct products that **don’t have a common interface**. Therefore, you don’t know what would be the return type for such a method. However, if you’re dealing with products from a single hierarchy, the fetching method can be safely added to the base interface.
        
    4. Think about creating a **director** class. It may encapsulate various ways to construct a product using the same builder object.
    5. The **client code** creates both the **builder** and the **director** objects. Before construction starts, the client must pass a **builder** object **to** the **director**. Usually, the client does this only once, via parameters of the director’s class constructor. The director uses the builder object in all further construction. There’s an **alternative approach**, where the **builder** is passed to a specific product construction method of the director.
    6. The construction result can be obtained directly from the **director** only if all products follow the same interface. Otherwise, the client should fetch the result from the **builder**.
- The Builder pattern can be **recognized** in a class, which has a **single creation** method and **several methods to configure** the resulting object. Builder methods often support **chaining** (for example, `someBuilder.setValueA(1).setValueB(2).create()`).

**👍 Advantages 👍**

- You can construct objects **step-by-step**, defer construction steps or run steps recursively.
- You can **reuse** the **same construction code** when building various representations of products.
- **Single Responsibility Principle**. You can isolate complex construction code from the business logic of the product.

**👎 Disadvantages 👎**

- The overall **complexity** of the code **increases** since the pattern requires creating **multiple new classes**.

**↔️ Alternatives ↔️**

- 

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- 

**🛑 Worst practices 🛑**

- 

Sources:

### **Prototype**

**🔽 What? 🔽**

- a creational design pattern that lets you **copy existing objects** without making your code dependent on their classes.

**🔁 What does it do? 🔁**

- delegates the cloning process to the **actual objects** that are being cloned.

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- you have an object, and you want to create an **exact copy of it**. Sometimes you only know the **interface** that the object follows, but **not** its concrete **class**, when, for example, a parameter in a method accepts any objects that follow some interface.
- when your code **shouldn’t depend on** the concrete **classes** of objects that you **need to copy**.
- to **reduce the number** of **subclasses** that only **differ in the way they initialize** their respective objects.

🤔 **How does it work?** 🤔

- This interface lets you clone an object **without coupling** your code to the class of that object.
- An **object that supports cloning** is called a ***prototype***.

- Designs that make heavy use of **Composite** and **Decorator** can often **benefit** from using **Prototype**. Applying the pattern **lets you clone complex structures** instead of **re-constructing them from scratch**.
- 

- **Prototype** can help when you need to save copies of **Commands** in**to history**.

**✍️ How to use it? ✍️**

- Usually, such an interface contains just a single `clone` method.
- **Prototype** isn’t based on **inheritance**, so it doesn’t have its drawbacks. On the other hand, Prototype requires a **complicated initialization** of the **cloned object**. **Factory Method** is based on **inheritance** but **doesn’t require an initialization step**.
- The Prototype pattern is available in Python out of the box with a `copy` module. The prototype can be easily recognized by a `clone` or `copy` methods, etc.
- **How to Implement**
    1. Create the **prototype interface** and **declare the `clone` method** in it. Or just **add the method to all classes** of an existing class hierarchy, if you have one.
    2. A prototype class must define the **alternative constructor** that accepts an **object** of that class as an **argument**. The **constructor must copy the values** of all **fields** defined in the class from the passed object into the newly created instance. If you’re **changing** a **subclass**, you must **call the parent constructor** to let the superclass handle the cloning of its private fields.
        
        If your programming language doesn’t support method overloading, you won’t be able to create a separate “prototype” constructor. Thus, copying the object’s data into the newly created clone will have to be performed within the `clone` method. Still, having this code in a regular constructor is safer because the resulting object is returned fully configured right after you call the `new` operator.
        
    3. The cloning method usually consists of just one line: running a `new` operator with the prototypical version of the constructor. Note, that every **class must explicitly override the cloning method** and use its own class name along with the `new` operator. Otherwise, the cloning method may produce an object of a parent class.
    4. Optionally, create a **centralized prototype registry** to store a **catalog of frequently used prototypes**.
        
        You can implement the registry as a new **factory class** or put it in the base prototype class with a static method for fetching the prototype. This method should search for a prototype based on search criteria that the client code passes to the method. The criteria might either be a simple string tag or a complex set of search parameters. After the appropriate prototype is found, the registry should clone it and return the copy to the client.
        
        Finally, replace the direct calls to the subclasses’ constructors with calls to the factory method of the prototype registry.
        

**👍 Advantages 👍**

- You can clone objects **without coupling** to their concrete **classes**.
- You can get rid of **repeated initialization code** in favor of cloning pre-built prototypes.
- You can produce complex objects more conveniently.
- You get an **alternative to inheritance** when dealing with configuration presets for complex objects.

**👎 Disadvantages 👎**

- Doesn’t make sense, if you have only 2-3 subclasses, it is better to use when you need to implemet too simmilar subclasses definitions.
- Cloning complex objects that have **circular references** might be very tricky.

**↔️ Alternatives ↔️**

- Subclassing

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- 

**🛑 Worst practices 🛑**

- 

Sources:

[Prototype](https://refactoring.guru/design-patterns/prototype)

### **Singleton**

**🔽 What? 🔽**

- creational design pattern that lets you ensure that a class has **only one instance**, while providing a **global access point to this instance**.

**🔁 What does it do? 🔁**

- 

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- to ensure that a class has only a single instance.
- it also protects that instance from being overwritten by other code.
- when you need **stricter control** over **global** variables

🤔 **How does it work?** 🤔

- You gain a global access point to that instance.
- The Singleton pattern **disables** all other means of **creating objects** of a class except for the **special creation method**. This method either creates a new object or returns an existing one if it has already been created.
- **Abstract Factories, Builders and Prototypes** can all be implemented as **Singletons**.
- A **Facade class** can often be transformed into a Singleton since a single facade object **is sufficient in most cases**.

**✍️ How to use it? ✍️**

- All **implementations** of the Singleton have these two **steps** in common:
    - Make the **default constructor private**, to prevent other objects from using the `new` operator with the Singleton class.
    - Create a **static creation method** that **acts** as a **constructor**. Under the hood, this method calls the private constructor to create an object and saves it in a static field. **All following calls** to this method return the **cached object**.
- **How to Implement**
    1. Declare a **public static creation method** for **getting** the **singleton instance**.
    2. Implement “lazy initialization” inside the static method. It should **create a new object** on its **first call** and put it into the static field. The method should always return that instance on all subsequent calls.
    3. Make the **constructor of the class private**. The static method of the class will still be able to call the constructor, but not the other objects.
    4. Go over the client code and **replace all direct calls** to the singleton’s constructor with calls to its **static creation method**.

**👍 Advantages 👍**

- The singleton object is initialized **only** when it’s requested for the first time.
- Unlike **global variables**, the Singleton pattern **guarantees** that there’s just **one instance of a class** in a sync code. Nothing, except for the Singleton class itself, can replace the cached instance.

**👎 Disadvantages 👎**

- **Violates** the **Single Responsibility Principle**. The pattern solves two problems at the time.
- The Singleton pattern can mask bad design, for instance, when the **components of the program know too much about each other**.
- The pattern requires **special treatment in a multithreaded environment** so that multiple threads won’t create a singleton object several times.
- It may be difficult to **unit test** the client code of the Singleton because many test frameworks rely on inheritance when producing mock objects. Since the constructor of the singleton class is private and overriding static methods is impossible in most languages, you will need to think of a creative way to mock the singleton. Or just don’t write the tests. Or don’t use the Singleton pattern.

**↔️ Alternatives ↔️**

- Global variables

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- a single database object shared by different parts of the program.

**🛑 Worst practices 🛑**

- 

Sources:

[Singleton Design Pattern - Advanced Python Tutorial #9](https://www.youtube.com/watch?v=Qb4rMvFRLJw)

## **Structural Design Patterns**

**🔽 What? 🔽**

- Design patterns

**🔁 What does it do? 🔁**

- explain how to assemble objects and classes into **larger structures**, while keeping these structures **flexible** and **efficient**.

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- when you need to **compose** objects and classes into **larger structures** while **keeping them flexible and efficient**.
- for **clarifying relationships between classes**, **managing object hierarchies**, and **altering interfaces** **without affecting clients**.
- Structural patterns promote **code reuse**, **simplify system design**, and **enhance scalability**.
- They're beneficial when dealing with **complex systems**, **integration of new components**, or **refactoring existing codebases**.

🤔 **How does it work?** 🤔

- 

**✍️ How to use it? ✍️**

- 

**👍 Advantages 👍**

- 

**👎 Disadvantages 👎**

- 

**↔️ Alternatives ↔️**

- 

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- 

**🛑 Worst practices 🛑**

- 

Sources:

[Design Patterns Cheat Sheet - When to Use Which Design Pattern? - GeeksforGeeks](https://www.geeksforgeeks.org/system-design/design-patterns-cheat-sheet-when-to-use-which-design-pattern/)

[Structural Design Patterns](https://refactoring.guru/design-patterns/structural-patterns)

### Adapter

**🔽 What? 🔽**

- structural design pattern

**🔁 What does it do? 🔁**

- allows objects with incompatible interfaces to collaborate.

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- when you want to **use some existing class**, but **its interface** **isn’t compatible** with the rest of your code.
- when you want to **reuse several existing subclasses** that **lack** some **common functionality** that **can’t be added** to the **superclass**.

🤔 **How does it work?** 🤔

- a special object that **converts the interface** of one object so that another object can understand it.
- The Adapter pattern lets you create a **middle-layer class** that serves as a **translator** between your **code** and a **legacy class**, a 3rd-party class or any other class with a weird interface.
- An adapter **wraps one of the objects** to hide the complexity of conversion happening behind the scenes. The wrapped object isn’t even aware of the adapter. For example, you can wrap an object that operates in meters and kilometers with an adapter that converts all of the data to imperial units such as feet and miles.
- Here’s how it works:
    1. The adapter gets an interface, compatible with **one of the existing objects**.
    2. Using this **interface**, the existing object can safely call the **adapter’s methods**.
    3. Upon receiving a call, the adapter passes the request to the second object, but in a format and order that the second object expects.
- The **Class Adapter** **doesn’t need to wrap** any objects because it **inherits** behaviors from **both the client and the service**. The adaptation happens within the **overridden methods**. The resulting adapter can be used in place of an existing client class.
- Adapter is recognizable by a **constructor** which takes an **instance** of a **different abstract/interface type**. When the adapter **receives a call to any of its methods**, it **translates parameters** to the appropriate format and **then directs the call** to one or several **methods** of the **wrapped object**.

- Adapter provides a **completely different interface** for accessing an existing object. On the other hand, with the **Decorator** pattern the interface either **stays the same** or **gets extended**. In addition, **Decorator supports recursive composition**, which **isn’t possible** when you use **Adapter**.

- **Facade** defines a **new interface for existing objects**, whereas Adapter tries to make the **existing interface usable**. Adapter usually wraps just one object, while Facade works with an **entire subsystem of objects**.
- 

- Bridge is usually designed **up-front**, letting you develop parts of an application **independently** of each other. On the other hand, **Adapter** is commonly used with an **existing app to make some otherwise-incompatible** classes work together nicely.

**✍️ How to use it? ✍️**

- **How to Implement**
    1. Make sure that you have **at least two classes** with incompatible interfaces:
        - A useful *service* class, which **you can’t change** (often 3rd-party, legacy or with lots of existing dependencies).
        - **One or several *client* classes** that would **benefit from using the service class**.
    2. Declare the **client interface** and **describe how clients communicate** with the service.
    3. Create the **adapter class** and make it **follow the client interface**. Leave all the methods empty for now.
    4. Add a field to the adapter class to **store a reference** to the service object. The common practice is to **initialize this field via the constructor**, but sometimes it’s more convenient to pass it to the adapter when calling its methods.
    5. One by one, **implement all methods** of the **client** interface in the **adapter class**. The adapter should **delegate most of the real work to the service object**, handling only the **interface** or **data format conversion**.
    6. Clients should use the adapter via the **client interface**. This will let you change or extend the adapters **without affecting the client code**.

**👍 Advantages 👍**

- **Single Responsibility Principle**. You can separate the interface or data conversion code from the primary business logic of the program.
- **Open/Closed Principle**. You can introduce new types of adapters into the program without breaking the existing client code, as long as they work with the adapters through the client interface.

**👎 Disadvantages 👎**

- The overall **complexity of the code increases** because you need to introduce a **set of new interfaces and classes**. Sometimes it’s simpler just to change the service class so that it matches the rest of your code.

**↔️ Alternatives ↔️**

- Decorator pattern.

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- XML-to-JSON adapters

**🛑 Worst practices 🛑**

- 

Sources:

[Adaptor Pattern Explained Simply | Programming and Design Patterns in Python](https://www.youtube.com/watch?v=kjkfbagw7iE)

[Adapter](https://refactoring.guru/design-patterns/adapter)

### **Bridge**

**🔽 What? 🔽**

- structural design pattern

**🔁 What does it do? 🔁**

- 

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- when you want to divide and organize a **monolithic class** that has **several variants of some functionality** (for example, if the class can work with **various database servers**). The Bridge pattern lets you **split the monolithic class** into **several class hierarchies**. After this, you can change the classes in each hierarchy independently of the classes in the others.
- when you need to **extend a class in several orthogonal (independent) dimensions**.
- you need to be able to switch implementations at runtime.

🤔 **How does it work?** 🤔

- You can prevent the explosion of a class hierarchy by transforming it into several related hierarchies.
    
    ![image.png](OOP/image%203.png)
    
- **Abstraction** (also called **interface**) is a **high-level control layer** for some entity. This layer isn’t supposed to do any real work on its own. It should **delegate the work** to the **implementation layer** (also called platform).
- The **abstraction** may **list the same methods** as the **implementation**, but usually the **abstraction declares some complex behaviors** that rely on a wide **variety of primitive operations** declared by the **implementation**.
- Mental Example with a Pseudocode
    
    The original class hierarchy is divided into two parts: devices and remote controls.
    
    ![image.png](OOP/image%204.png)
    
- 

**✍️ How to use it? ✍️**

- split a large class or a set of closely related classes into **two separate hierarchies**—**abstraction and implementation**—which can be **developed independently** of each other.
- **How to Implement**
    1. Identify the **orthogonal dimensions** in your classes. These independent concepts could be: abstraction/platform, domain/infrastructure, front-end/back-end, or interface/implementation.
    2. See what **operations the client needs** and **define** them **in** the **base abstraction class**.
    3. Determine the **operations** available on **all platforms**. Declare the ones that the abstraction needs in the **general implementation interface**.
    4. For all platforms in your domain **create concrete implementation classes**, but make sure they all **follow the implementation interface**.
    5. Inside the **abstraction class**, add a **reference field** for the **implementation type**. The **abstraction delegates most of the** **work** to the implementation object that’s referenced **in that field**.
    6. If you have several **variants of high-level logic**, create refined abstractions for each variant by **extending the base abstraction class**.
    7. The client code should pass an **implementation object to the abstraction’s constructor** to associate one with the other. After that, the client can **forget about the implementation** and work only with the **abstraction object**.

**👍 Advantages 👍**

- You can create **platform-independent** classes and apps.
- The client code works with **high-level abstractions**. It isn’t exposed to the platform details.
- **Open/Closed Principle**. You can introduce new abstractions and implementations independently from each other. This approach simplifies **code maintenance** and **minimizes the risk of breaking existing code**.
- **Single Responsibility Principle**. You can focus on high-level logic in the abstraction and on platform details in the implementation.

**👎 Disadvantages 👎**

- You might make the **code more complicated** by applying the pattern to a highly cohesive class.

**↔️ Alternatives ↔️**

- 

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- cross-platform apps
- supporting multiple types of database servers
- working with several API providers of a certain kind (for example, cloud platforms, social networks, etc.)

**🛑 Worst practices 🛑**

- 

Sources:

[Bridge](https://refactoring.guru/design-patterns/bridge)

### Composite

**🔽 What? 🔽**

- structural design pattern

**🔁 What does it do? 🔁**

- 

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- compose objects into **tree structures** and then work with these structures as if they were **individual objects**.
- only when the core model of your app can be represented as a **tree**.
- when you want the client code to **treat both simple and complex elements uniformly**.

🤔 **How does it work?** 🤔

- Pattern Structure Flow
    - The **Component** interface describes **operations** that are common to both **simple** and **complex elements** of the tree.
    - The **Leaf** is a basic element of a tree that **doesn’t have sub-elements**. Usually, leaf components end up doing **most of the real work**, since they **don’t have anyone to delegate the work to**.
    - The **Container** (aka **composite/branch**) is an element that **has sub-elements**: leaves or other containers. A container doesn’t know the concrete classes of its children. It works with all sub-elements only via the **component interface**.
    - Upon receiving a request, a container **delegates the work to its sub-elements**, processes intermediate results and then returns the final result to the client.
    - The **Client works** with all elements **through** the **component** interface. As a result, the client can work in the same way with both **simple or complex elements** of the tree.
- The Composite pattern provides you with two basic element types that share a common interface: **simple leaves and complex containers**. A container can be composed of both leaves and other containers. This lets you construct a **nested recursive object structure** that **resembles a tree**.
- 

- You can **use** Iterators to traverse **Composite trees**.

- Chain of Responsibility is often used in conjunction with **Composite**. In this case, when a **leaf component** gets a request, it may **pass it** **through the chain** of all of the parent components **down** to the root of the object tree.

**✍️ How to use it? ✍️**

- How to Implement
    1. Make sure that the **core model** of your app can be **represented as a tree structure**. Try to break it down into simple elements and containers. Remember that **containers must be able to contain both simple elements and other containers**.
    2. Declare the **component interface** with a list of methods that make sense for both **simple and complex components**.
    3. Create a **leaf** class to **represent simple elements**. A program may have **multiple different leaf classes**.
    4. Create a **container class** to represent complex elements. In this class, provide an array field for storing references to sub-elements. The array must be able to store **both leaves and containers**, so make sure it’s declared with the **component interface type**.
    While implementing the methods of the **component interface**, remember that a container is supposed to be **delegating most of the work** to **sub-elements**.
    5. Finally, define the methods for **adding** and **removal** of **child elements** in the **container**.
    Keep in mind that these operations can be **declared in the component interface**. This would **violate** the **Interface Segregation Principle** because the methods will be empty in the leaf class. However, the client will be able to treat all the elements equally, even when composing the tree.

**👍 Advantages 👍**

- You can work with **complex tree structures more conveniently**: use **polymorphism** and **recursion** to your advantage.
- **Open/Closed Principle**. You can introduce new element types into the app without breaking the existing code, which now works with the object tree.

**👎 Disadvantages 👎**

- It might be **difficult** to **provide a common interface** for classes whose **functionality differs too much**. In certain scenarios, you’d need to overgeneralize the component interface, making it harder to comprehend.

**↔️ Alternatives ↔️**

- 

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- 

**🛑 Worst practices 🛑**

- 

Sources:

[Composite](https://refactoring.guru/design-patterns/composite)

### **Decorator**

**🔽 What? 🔽**

- structural design pattern
- “Wrapper” is the alternative nickname

**🔁 What does it do? 🔁**

- 

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- to **attach** new **behaviors** to objects by placing these objects inside **special wrapper objects** that contain the **behaviors**.
- when you need to be able to assign **extra behaviors to objects** at runtime **without breaking the code** that uses these objects.
- when it’s awkward or **not possible** to **extend** an **object’s behavior** using **inheritance**.

🤔 **How does it work?** 🤔

- The Decorator lets you structure your business logic into **layers**, create a **decorator for each layer** and compose objects with various combinations of this logic at runtime. The client code can treat all these objects in the same way, since they all follow a **common interface**.
- A **wrapper** is an object that can be **linked** with some **target object**. The wrapper **contains** the same **set of methods** as the **target** and delegates to it all requests it receives. However, the wrapper may alter the result by doing something **either before or after it** passes the **request to the target**.
- The **Component** declares the common interface for both **wrappers and wrapped objects**.
    - **Concrete Component** is a class of objects **being wrapped**. It defines the basic behavior, which **can be altered by decorators**.
- The **Base Decorator** class has a field for **referencing a wrapped object**. The field’s **type** should be declared as the **component interface** so it can contain both **concrete components and decorators**. The base decorator **delegates all operations** to the **wrapped object**.
    - **Concrete Decorators** define extra behaviors that **can be added to components dynamically**. Concrete decorators **override methods** of the **base decorator** and execute their behavior **either before or after calling** the **parent method**.
- The **Client** can wrap components in **multiple layers of decorators**, as long as it works with all objects via the component interface.
- **Composite and Decorator** have similar structure diagrams since **both rely on recursive composition** to organize an open-ended number of objects.
    
    A Decorator is like a Composite but **only has one child component**. There’s another significant difference: Decorator adds **additional responsibilities to the wrapped object**, while Composite just “**sums up**” its children’s results.
    
    However, the patterns can also **cooperate**: you can use Decorator to extend the behavior of a specific object in the Composite tree.
    
- Decorator can be recognized by **creation methods or constructors** that **accept objects of the same class** or interface as a **current class**.
- 

- **Decorator and Proxy** have similar structures, but very different **intents**. Both patterns are built on the **composition principle**, where one **object** is supposed to **delegate** some of the **work** to **another**. The difference is that a **Proxy** usually manages the **life cycle of its service** object **on its own**, whereas the composition of **Decorators** is **always controlled by the client**.

- Chain of Responsibility and **Decorator** have very similar class structures. Both patterns rely on **recursive composition** to pass the execution through a series of objects. However, there are several crucial differences. The CoR handlers can execute arbitrary operations independently of each other. They can also stop passing the request further at any point. On the other hand, various **Decorators** can **extend** the **object’s behavior** while keeping it **consistent** with the **base interface**. In addition, decorators **aren’t allowed** to **break the flow of the request**.

**✍️ How to use it? ✍️**

- How to Implement
    1. Make sure your business **domain** can be represented as a primary component with **multiple optional layers over it**.
    2. Figure out **what methods are common** to both the **primary** component and the **optional layers**. Create a **component interface** and **declare those methods there**.
    3. Create a **concrete component class** and define the **base behavior** in it.
    4. Create a **base decorator class**. It should have a **field for storing** a reference to a **wrapped object**. The field should be declared with the **component interface type** to allow linking to concrete components as well as decorators. The base decorator must delegate all work to the wrapped object.
    5. Make sure all **classes implement** the **component interface**.
    6. Create **concrete decorators** by **extending** them from the **base decorator**. A concrete decorator must **execute its behavior** before or after the call to the **parent method** (which always delegates to the wrapped object).
    7. The **client code** must be responsible for **creating decorators** and composing them in the way the client needs.

**👍 Advantages 👍**

- You can extend an object’s behavior **without making** a **new subclass**.
- You can **add or remove responsibilities** from an object at runtime.
- You can **combine several behaviors** by wrapping an object into **multiple decorators**.
- **Single Responsibility Principle**. You can divide a monolithic class that implements many possible variants of behavior into several smaller classes.
- Supports **recursive composition**, which isn’t possible when you use **Adapter**.

**👎 Disadvantages 👎**

- It’s hard to **remove a specific wrapper** from the wrappers stack.
- It’s **hard** to implement a decorator in such a way that its behavior doesn’t depend on the **order** in the decorators stack.
- The **initial configuration** code of layers might look pretty **ugly**.

**↔️ Alternatives ↔️**

- Adapter
- Subclassing

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- The Decorator is pretty standard in Python code, especially in code related to **streams**.

**🛑 Worst practices 🛑**

- 

Sources:

[Decorator](https://refactoring.guru/design-patterns/decorator)

### Facade

**🔽 What? 🔽**

- structural design pattern

**🔁 What does it do? 🔁**

- provides a **simplified interface** to a library, a framework, or any other complex set of classes.

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- especially handy when working with complex libraries and APIs.
- when you need to **integrate** your app with a sophisticated **library** that has **dozens of features**, but you just need a **tiny bit of its functionality**.
- when you need to have a **limited but straightforward interface** to a **complex subsystem**.
- when you want to structure a subsystem **into layers**.
- Create facades to **define entry points** to **each level of a subsystem**. You can **reduce coupling between multiple subsystems** by requiring them to communicate only through facades.

🤔 **How does it work?** 🤔

- Facade can be recognized in a class that has a **simple interface**, but delegates most of the work to **other classes**. Usually, facades **manage the full life cycle** of objects they use.
- Pattern Structure Flow
    - A facade is a **class** that provides a **simple interface** to a **complex subsystem** which contains **lots of moving parts**. A facade might provide **limited functionality** in comparison to working with the subsystem directly. However, it includes only those features that **clients really care about**.
    - The **Facade** provides convenient access to a **particular part of the subsystem’s functionality**. It knows where to direct the client’s request and how to operate all the moving parts.
    - An **Additional Facade** class can be created **to prevent polluting a single facade** with unrelated features that might make it yet another **complex structure**. Additional facades can be used by both **clients and other facades**.
    - The **Complex Subsystem** consists of dozens of various objects. To make them all do something meaningful, you have to dive deep into the subsystem’s implementation details, such as initializing objects in the correct order and supplying them with data in the proper format.
    - **Subsystem classes** aren’t aware of the facade’s existence. They operate within the system and **work with each other directly**.
    - The **Client** uses the facade **instead of calling the subsystem objects** directly.

- Facade and Mediator have **similar jobs**: they try to organize collaboration between lots of tightly coupled classes.
    - Facade defines a **simplified interface** to a subsystem of objects, but it **doesn’t introduce any new functionality**. The subsystem itself is unaware of the facade. Objects within the subsystem can communicate directly.
    - Mediator **centralizes communication** between components of the system. The components **only know** about the **mediator object** and don’t communicate directly.
- Mental Example
    
    ![image.png](OOP/image%205.png)
    

**✍️ How to use it? ✍️**

- **How to Implement**
    1. Check whether it’s possible to provide a **simpler interface** than what an existing subsystem already provides. You’re on the right track if this interface makes the client code independent from many of the subsystem’s classes.
    2. Declare and implement this interface in a **new facade class**. The facade should redirect the calls from the client code to **appropriate objects of the subsystem**. The facade should be responsible for initializing the subsystem and managing its further life cycle unless the client code already does this.
    3. To get the full benefit from the pattern, make all the client code communicate with the subsystem **only via the facade**. Now the client code is protected from any changes in the subsystem code. For example, when a subsystem gets upgraded to a new version, you will only need to **modify the code in the facade**.
    4. If the facade becomes **too big**, consider extracting part of its behavior to a new, refined facade class.

**👍 Advantages 👍**

- You can isolate your code from the complexity of a subsystem.

**👎 Disadvantages 👎**

- A facade can become a **god object** coupled to all classes of an app.

**↔️ Alternatives ↔️**

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- 

**🛑 Worst practices 🛑**

- 

Sources:

[Facade](https://refactoring.guru/design-patterns/facade)

### Flyweight

**🔽 What? 🔽**

- structural design pattern

**🔁 What does it do? 🔁**

- 

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- to **fit** more objects into the available amount of RAM by **sharing common parts of state** between multiple objects **instead of keeping all of the data** in **each object**.

🤔 **How does it work?** 🤔

- 

**✍️ How to use it? ✍️**

- 

**👍 Advantages 👍**

- You can save lots of RAM, assuming your program has tons of similar objects.

**👎 Disadvantages 👎**

- You might be trading **RAM over CPU cycles** when some of the context data needs to be **recalculated** each time somebody calls a **flyweight method**.
- The code becomes much more **complicated**. New team members will always be wondering why the state of an entity was separated in such a way.

**↔️ Alternatives ↔️**

- 

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- 

**🛑 Worst practices 🛑**

- 

Sources:

[Flyweight](https://refactoring.guru/design-patterns/flyweight)

### **Proxy**

**🔽 What? 🔽**

- structural design pattern

**🔁 What does it do? 🔁**

- 

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- to provide a substitute or placeholder for another object. A proxy **controls access** to the original object, allowing you to perform something either **before or after the request gets** through to the **original object**.
- **Lazy initialization** (**virtual** proxy). This is when you have a **heavyweight service** object that wastes system resources by being always up, even though you only **need it from time to time**. Instead of creating the object when the app launches, you can delay the object’s initialization to a time when it’s really needed.
- **Access control** (**protection** proxy). This is when you want only **specific clients** to be able to use the **service object**; for instance, when your objects are crucial parts of an operating system and clients are various launched applications (including malicious ones). The **proxy** can **pass** the request to the **service object** only if the **client’s credentials match some criteria**.
- **Logging** requests (**logging** proxy). This is when you want to keep a history of requests to the service object. The proxy can **log each request before passing it to the service**.
- **Caching** request results (**caching** proxy). This is when you need to **cache results of client requests** and **manage the life cycle of this cache**, especially if **results are quite large**. The proxy can implement **caching** for **recurring requests** that **always yield** the **same results**. The proxy may use the **parameters** of requests as the **cache keys**.
- **Smart reference**. This is when you need to be able to dismiss a **heavyweight** object once there are no clients that use it. The proxy can **keep track of clients** that obtained a reference to the service object or its results. From time to time, the proxy may go over the clients and check whether **they are still active**. If the client list gets empty, the **proxy might dismiss the service object** and **free the underlying system resources**. The proxy can also **track** whether the **client** had **modified** the **service object**. Then the **unchanged objects** may be **reused by other clients**.

🤔 **How does it work?** 🤔

- A **proxy receives client requests**, does some **work** (access control, caching, etc.) and then **passes the request** to a service object.
- The **Proxy pattern** suggests that you create a new **proxy class** with the **same interface** as an **original service object**. Then you update your app so that it **passes** the **proxy object** to **all of the original object’s clients**. Upon receiving a request from a client, the proxy creates a real service object and delegates all the work to it.
- With **Adapter** you access an **existing object** via **different interface**. With **Proxy**, the **interface** stays the **same**. With Decorator you **access the object** via an **enhanced interface**.
- **Facade** is similar to Proxy in that **both buffer a complex entity** and **initialize it on its own**. Unlike Facade, **Proxy** has the **same interface** as its **service object**, which makes them **interchangeable**.

**✍️ How to use it? ✍️**

- The **Service Interface** declares the interface of the Service. The **proxy must follow this interface** to be able to disguise itself as a service object.
- The **Service is a class** that provides some **useful business logic**.
- The **Proxy class** has a reference field that points to a **service object**. After the proxy finishes its processing (e.g., lazy initialization, logging, access control, caching, etc.), it **passes the request to the service object**.
    
    Usually, proxies manage the **full lifecycle of their service objects**.
    
- The **Client** should work with both services and proxies via the same interface. This way you can pass a proxy into any code that expects a service object.
- **How to Implement**
    1. If there’s no **pre-existing service interface**, **create** one to make proxy and service objects interchangeable. Extracting the interface from the service class isn’t always possible, because you’d need to change all of the service’s clients to use that interface. Plan B is to make the **proxy a subclass of the service class**, and this way it’ll inherit the interface of the service.
    2. Create the **proxy class**. It should have a field for **storing a reference to the service**. Usually, proxies create and manage the **whole life cycle of their services**. On rare occasions, a **service is passed to the proxy** via a **constructor by the client**.
    3. Implement the **proxy methods** according to their purposes. In most cases, after doing some work, the **proxy should delegate the work** to the **service object**.
    4. Consider introducing a **creation method** that decides whether the client gets a proxy or a real service. This can be a simple static method in the proxy class or a full-blown factory method.
    5. Consider implementing **lazy initialization** for the service object.

**👍 Advantages 👍**

- You can **control the service object without clients knowing about** it.
- You can **manage the lifecycle of the service** object when **clients don’t care** about it.
- The proxy works even if the **service object isn’t ready** or is not available.
- **Open/Closed Principle**. You can introduce new proxies without changing the service or clients.

**👎 Disadvantages 👎**

- The **code** may become **more complicated** since you need to **introduce** a **lot of new classes**.
- The **response from the service** might get **delayed**.

**↔️ Alternatives ↔️**

- 

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- 

**🛑 Worst practices 🛑**

- 

Sources:

[Proxy](https://refactoring.guru/design-patterns/proxy)

[Proxy - Design Patterns in 5 minutes](https://www.youtube.com/watch?v=t5zunzg2sr8)

## **Behavioral Design Patterns**

**🔽 What? 🔽**

- design patterns

**🔁 What does it do? 🔁**

- are concerned with algorithms and the assignment of **responsibilities between objects**.

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- when you need to **manage algorithms, communication, or responsibilities between objects**.
- for **encapsulating behavior** that varies and **promoting loose coupling between objects**.
- to facilitate **code reuse**, **flexibility**, and **maintainability** by defining how objects interact and communicate.
- to address scenarios like **handling complex workflows**, **managing state transitions**, or **implementing communication between objects**.

🤔 **How does it work?** 🤔

- 

**✍️ How to use it? ✍️**

- 

**👍 Advantages 👍**

- 

**👎 Disadvantages 👎**

- 

**↔️ Alternatives ↔️**

- 

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- 

**🛑 Worst practices 🛑**

- 

Sources:

[Design Patterns Cheat Sheet - When to Use Which Design Pattern? - GeeksforGeeks](https://www.geeksforgeeks.org/system-design/design-patterns-cheat-sheet-when-to-use-which-design-pattern/)

[Behavioral Design Patterns](https://refactoring.guru/design-patterns/behavioral-patterns)

### **Chain of Responsibility**

**🔽 What? 🔽**

- behavioral design pattern

**🔁 What does it do? 🔁**

- allows multiple objects to handle the request **without coupling** *sender* class to the **concrete classes** of the *receivers*.

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- to pass requests along a **chain of handlers**. Upon receiving a request, each handler **decides** either to **process the request** or to **pass** it to the **next handler in the chain**.
- when your program is expected to process **different kinds of requests** in **various ways**, but the **exact types** of requests and their sequences are **unknown beforehand**. 
The pattern lets you link several handlers into one chain and, upon receiving a request, **“ask” each handler** whether **it can process it**. This way all handlers get a chance to process the request.
- when it’s essential to **execute several handlers in a particular order**.
Since you can link the handlers in the chain in any **order**, all requests will get through the chain exactly as **you planned**.
- when the **set of handlers** and their **order** are **supposed to change** at runtime. 
If you provide **setters** for a reference field inside the handler classes, you’ll be able **to insert, remove** or **reorder** handlers dynamically.

🤔 **How does it work?** 🤔

- Chain of Responsibility relies on **transforming particular behaviors** in**to stand-alone objects** called **handlers**. In our case, each check should be **extracted to its own class** with a **single method** that **performs the check**. The request, along **with its data**, is **passed** to this **method** as an **argument**.
    
    The pattern suggests that you **link these handlers** into a **chain**. Each **linked handler** has a **field** for **storing a reference** to the **next handler in the chain**. In addition to processing a request, **handlers** **pass** the request **further along the chain**. The request travels along the chain until **all handlers** have had a chance to **process it**.
    
    Here’s the best part: a **handler** can decide **not to pass** the request further down the chain and effectively **stop any further processing**.
    
    In our example with ordering systems, a handler performs the processing and then decides whether to pass the request further down the chain. Assuming the request **contains the right data**, all the handlers can execute their primary behavior, whether it’s authentication checks or caching.
    
- Ordering System Mental Example. Handlers are lined up one by one, forming a chain.
    
    ![image.png](OOP/image%206.png)
    
- It’s crucial that **all handler classes** implement the **same interface**. Each **concrete handler** should only care about the **following one having** the `execute` method. This way you can **compose chains** at runtime, using various handlers without coupling your code to their concrete classes.
- The chain can be **composed dynamically** at runtime with any handler that follows a standard handler interface.
- Pattern Structure Flow
    - The **Handler** declares the **interface**, common for **all concrete handlers**. It usually contains just a **single method for handling requests**, but sometimes it may also have **another method for setting** the **next handler on the chain**.
    - The **Base Handler** is an **optional** class where you can put the **boilerplate code** that’s **common to all handler classes**.
        
        Usually, this class defines a **field for storing a reference to the next handler**. The clients can build a chain by passing a handler to the constructor or setter of the previous handler. The class may also implement the **default handling behavior**: it can pass execution to the **next handler** after **checking for its existence**.
        
    - **Concrete Handlers** contain the actual code for processing requests. Upon receiving a request, each handler must decide whether to process it and, additionally, **whether to pass it along the chain**.
        
        **Handlers** are usually **self-contained** and **immutable**, accepting all necessary data just once via the constructor.
        
    - The **Client** may compose chains just once or compose them dynamically, depending on the application’s logic. Note that a request can **be sent to any handler in the chain**—it doesn’t have to be the first one.

- **Handlers** in **Chain of Responsibility** can be implemented as **Commands**. In this case, you can execute a lot of different operations over the same context object, represented by a request. However, there’s another approach, where the request itself is a **Command object**. In this case, you can execute the same operation in a series of different contexts **linked into a chain**.

- **Chain of Responsibility, Command, Mediator** and **Observer** address various ways of connecting **senders** and **receivers** of requests:
    - **Chain of Responsibility** passes a request **sequentially along a dynamic chain** of potential receivers **until one** of them **handles** it.
    - **Command** establishes **unidirectional connections** between **senders** and **receivers**.
    - **Mediator eliminate**s **direct connections** between senders and receivers, forcing them to **communicate indirectly** via a **mediator** object.
    - **Observer** lets **receivers dynamically subscribe** to and **unsubscribe** from receiving requests.

**✍️ How to use it? ✍️**

- **How to Implement**
    1. Declare the **handler interface** and describe the **signature** of a method for handling requests.
        
        **Decide** how the **client** will **pass the request** data into the **method**. The most flexible way is to **convert** the request into an **object** and pass it to the **handling method** as an **argument**.
        
    2. To eliminate duplicate boilerplate code in concrete handlers, it might be worth creating an **abstract base handler class**, derived from the **handler interface**.
        
        This class should have a field for **storing a reference** to the next handler in the chain. Consider **making the class immutable**. However, if you plan to modify chains at runtime, you need to define a **setter** for altering the value of the reference field.
        
        You can also implement the convenient **default behavior** for the handling method, which is to forward the request to the next object unless there’s none left. **Concrete handlers** will be able to **use this behavior** by calling the **parent method**.
        
    3. One by one create **concrete handler subclasses** and implement their handling methods. Each handler should make two decisions when receiving a request:
        - Whether it’ll **process the request**.
        - Whether it’ll pass the request **along the chain**.
    4. The **client** may either **assemble chains** on its own or receive **pre-built chains from other objects**. In the latter case, you must implement **some factory classes** to build chains according to the configuration or environment settings.
    5. The **client** may trigger **any handler** in the chain, not just the first one. The request will be passed along the chain until some handler refuses to pass it further or until it reaches the end of the chain.
    6. Due to the dynamic nature of the chain, the client should be ready to handle the following scenarios:
        - The chain **may** consist of a **single link**.
        - Some requests **may not reach** the **end** of the chain.
        - Others **may reach the end** of the chain **unhandled**.

**👍 Advantages 👍**

- You can control the **order of request handling**.
- **Single Responsibility Principle**. You can decouple classes that invoke operations from classes that perform operations.
- **Open/Closed Principle**. You can introduce new handlers into the app without breaking the existing client code.

**👎 Disadvantages 👎**

- Some requests may end up **unhandled**.

**↔️ Alternatives ↔️**

- Decorator

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- It’s mostly relevant when your code operates with chains of objects, such as **filters, event chains**, etc.
- For instance, when a **user clicks a button**, the event propagates **through the chain of GUI elements** that starts with the button, goes along its containers (like forms or panels), and ends up with the main application window. The event is processed by the first element in the chain that’s capable of handling it. This example is also noteworthy because it shows that a chain can always be **extracted from an object tree**.
    
    ![image.png](OOP/image%207.png)
    

**🛑 Worst practices 🛑**

- 

Sources:

[Chain of Responsibility](https://refactoring.guru/design-patterns/chain-of-responsibility)

### **Command**

**🔽 What? 🔽**

- behavioral design pattern

**🔁 What does it do? 🔁**

- converts requests or simple operations into objects.
- turns a request into a **stand-alone object** that **contains all** information about the **request**.

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- to pass **requests** as a **method arguments**, **delay** or queue a **request’s execution**, and support **undoable operations**.
- when you want to **parameterize objects with operations**. The Command pattern can turn a **specific method call** into a **stand-alone object**. This change opens up a lot of interesting uses: you can **pass commands** as **method arguments**, **store** them inside other objects, **switch linked commands** at runtime, etc. Here’s an example: you’re developing a GUI component such as a context menu, and you want your users to be able to configure menu items that trigger operations when an end user clicks an item.
- when you want to **queue operations**, **schedule their execution**, or **execute them remotely**. As with any other object, a command can be **serialized**, which means converting it to a string that can be easily written to a file or a database. Later, the string can be restored as the initial command object. Thus, you can delay and schedule command execution. But there’s even more! In the same way, you can **queue, log** or **send commands** over the network.
- when you want to implement **reversible operations**. Although there are many ways to implement **undo/redo**, the Command pattern is perhaps the **most popular of all**. To be able to revert operations, you **need to implement** the **history** of **performed operations**. The command history is a stack that **contains all executed command** objects along with related backups of the application’s state.

🤔 **How does it work?** 🤔

- Mental Example
    
    ![image.png](OOP/image%208.png)
    
- Pattern Structure
    1. The **Receiver** class contains some **business logic**. Almost any object may act as a receiver. Most **commands** only handle the details of **how** a request is **passed to the receiver**, while the **receiver** itself **does** the actual **work**.
    2. The **Command** **interface** usually declares just a **single method for executing** the command.
        1. **Concrete Commands** implement various **kinds of requests**. A concrete command isn’t supposed to perform the work on its own, but rather to **pass the call** to one of the business logic objects. However, for the sake of simplifying the code, these classes can be merged.
            
            **Parameters** required to **execute** a method on a **receiving object** can be declared as **fields** in the **concrete command**. You can make command objects **immutable** by only allowing the **initialization** of these fields **via the constructor**.
            
    3. The **Sender** class (aka *invoker*) is responsible for **initiating** requests. This class must have a field for storing a **reference** to a **command object**. The **sender triggers** that **command** instead of sending the request **directly to the receiver**. Note that the sender **isn’t responsible** for **creating** the **command object**. Usually, it gets a **pre-created command** from the client via the constructor.
    4. The **Client** **creates and configures** concrete command objects. The client must **pass** all of the **request parameters**, including a **receiver instance**, into the command’s constructor. After that, the resulting command may be associated with one or multiple senders.
- The Command pattern is recognizable by **behavioral methods** in an abstract/interface type (**sender**) which invokes a method in an implementation of a different abstract/interface type (**receiver**) which has been encapsulated by the **command implementation** during its creation. Command classes are usually limited to specific actions.
- 

- You can use **Command** and **Memento** together when implementing “**undo**”. In this case, **commands** are responsible for performing various operations over a target object, while **mementos** save the state of that object just before a command gets executed.

**✍️ How to use it? ✍️**

- **How to Implement**
    1. Declare the **command interface** with a single **execution method**.
    2. Start **extracting requests into concrete command** classes that implement the **command interface**. Each class must have a **set of fields** for storing the **request arguments** along with a **reference** to the actual **receiver** object. All these values must be **initialized** via the **command’s constructor**.
    3. Identify classes that will act as ***senders***. Add the fields for storing commands into these classes. Senders should **communicate with their commands** only via the command interface. Senders usually don’t create command objects on their own, but rather get them from the client code.
    4. Change the senders so they execute the command instead of sending a request to the receiver directly.
    5. The client should initialize objects in the following order:
        - Create receivers.
        - Create commands, and associate them with receivers if needed.
        - Create senders, and associate them with specific commands.

**👍 Advantages 👍**

- **Single Responsibility Principle**. You can decouple classes that invoke operations from classes that perform these operations.
- **Open/Closed Principle**. You can introduce new commands into the app without breaking existing client code.
- You can implement **undo/redo**.
- You can implement deferred execution of operations.
- You can assemble a set of **simple commands** in**to a complex one**.

**👎 Disadvantages 👎**

- Using Command pattern to implement reversible operations has two drawbacks.
    - First, it isn’t that easy to **save an application’s state** because some of it can be **private**. This problem can be mitigated with the **Memento** pattern.
    - Second, the state backups may consume quite a **lot** of **RAM**. Therefore, sometimes you can resort to an alternative implementation: instead of restoring the past state, the command performs the inverse operation. The reverse operation also has a price: it may turn out to be hard or even impossible to implement.
- The **code** may become **more complicated** since you’re introducing a whole new layer between senders and receivers.

**↔️ Alternatives ↔️**

- 

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- an alternative for callbacks to **parameterizing UI elements** with actions
- for **queueing tasks**
- **tracking** operations **history**

**🛑 Worst practices 🛑**

- 

Sources:

[Command Pattern Explained Simply | Programming and Design Patterns in Python](https://www.youtube.com/watch?v=A6E-S0v4Xt8)

[Command - Design Patterns in 5 minutes](https://www.youtube.com/watch?v=XW-gKMFbOyc)

[Command](https://refactoring.guru/design-patterns/command)

### **Iterator**

**🔽 What? 🔽**

- behavioral design pattern

**🔁 What does it do? 🔁**

- 

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- to traverse elements of a collection without exposing its underlying representation (list, stack, tree, etc.), without exposing its internal details.
- when your collection has a **complex data structure** under the hood, but you want to **hide its complexity from clients** (either for **convenience** or **security** reasons). The iterator **encapsulates** the details of working with a complex data structure, providing the client with several **simple methods** of accessing the collection elements. While this approach is very convenient for the client, it also protects the collection from **careless or malicious actions** which the client would be able to perform if working with the collection directly.
- to **reduce duplication** of the **traversal code** across your app. The code of non-trivial iteration algorithms tends to be very **bulky**. When placed within the business logic of an app, it may **blur the responsibility** of the original code and make it **less maintainable**. Moving the traversal code to designated iterators can help you make the code of the application **more lean and clean**.
- when you want your code to be able to traverse **different data structures** or when **types** of these **structures** are **unknown beforehand**. The pattern provides a couple of generic interfaces for both collections and iterators. Given that your code now uses these interfaces, it’ll still work if you pass it various kinds of collections and iterators that implement these interfaces.

🤔 **How does it work?** 🤔

- The main idea of the Iterator pattern is to **extract the traversal behavior** of a collection into a **separate object** called an **iterator**.
    
    ![Iterators implement various traversal algorithms. Several iterator objects can traverse the same collection at the same time.](OOP/image%209.png)
    
    Iterators implement various traversal algorithms. Several iterator objects can traverse the same collection at the same time.
    
- Pattern Structure Flow
    1. The **Iterator** **interface** declares the **operations required** for traversing a collection: fetching the **next** element, retrieving the **current position**, restarting iteration, etc.
        1. **Concrete Iterators** implement **specific algorithms** for **traversing** a **collection**. The iterator object should track the traversal progress on its own. This allows several iterators to traverse the same collection independently of each other.
    2. The **Collection** **interface** declares one or multiple **methods** for **getting iterators** compatible with the collection. Note that the return type of the methods must be declared as the **iterator interface** so that the concrete collections can return **various kinds** of **iterators**.
        1. **Concrete Collections** return new **instances** of a particular **concrete iterator** class each time the client requests one. 
    3. The **Client** works with both **collections** and **iterators** via their interfaces. This way the client isn’t coupled to concrete classes, allowing you to use various collections and iterators with the **same client code**. Typically, clients **don’t create iterators on their own**, but instead get them from collections. Yet, in certain cases, the client can create one directly; for example, when the client defines its **own special iterator**.

- You can use Memento along with **Iterator** to **capture** the **current iteration state** and **roll it back** if **necessary**.

**✍️ How to use it? ✍️**

- **How to Implement**
    1. Declare the **iterator interface**. At the very least, it must have a **method for fetching** the **next** element from a collection. But for the sake of convenience you can add a couple of other methods, such as fetching the previous element, tracking the current position, and checking the end of the iteration.
    2. Declare the **collection interface** and **describe a method for fetching iterators**. The return type should be **equal** to that of the **iterator interface**. You may declare similar methods if you plan to have several distinct groups of iterators.
    3. Implement **concrete iterator classes** for the collections that you want to be traversable with iterators. An iterator object must be linked with a **single collection instance**. Usually, this link is established via the **iterator’s constructor**.
    4. Implement the collection interface in your **collection classes**. The main idea is to provide the client with a shortcut for creating iterators, **tailored for a particular collection class**. The collection object must pass itself to the iterator’s constructor to establish a link between them.
    5. Go over the **client code** to replace all of the **collection traversal code** with the **use of iterators**. The client fetches a new iterator object each time it needs to iterate over the collection elements.

**👍 Advantages 👍**

- **Single Responsibility Principle**. You can clean up the client code and the collections by extracting bulky traversal algorithms into separate classes.
- **Open/Closed Principle**. You can implement new types of collections and iterators and pass them to existing code without breaking anything.
- You can iterate over the same collection in parallel because each iterator object contains **its own iteration state**. For the same reason, you **can delay** an iteration and **continue it when needed**.

**👎 Disadvantages 👎**

- Applying the pattern can be an overkill if your app only works with **simple collections**.
- Using an iterator may be **less efficient** than **going through** elements of some specialized collections **directly**.

**↔️ Alternatives ↔️**

- 

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- 

**🛑 Worst practices 🛑**

- 

Sources:

[Iterator](https://refactoring.guru/design-patterns/iterator)

### **Memento**

**🔽 What? 🔽**

- behavioral design pattern

**🔁 What does it do? 🔁**

- 

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- to **save** and **restore** the **previous state** of an object **without revealing** the details of its implementation.
- when you want to **produce snapshots** of the object’s state to be able to **restore a previous state** of the object. The Memento pattern lets you make **full copies of an object’s state**, including private fields, and store them separately from the object. While most people remember this pattern thanks to the “undo” use case.
- when direct access to the object’s fields/getters/setters **violates its encapsulation**. The Memento makes the object itself responsible for creating a snapshot of its state. No other object can read the snapshot, making the original object’s state data safe and secure.

🤔 **How does it work?** 🤔

- Pattern Structure Flow
    1. The **Originator** **class** can **produce snapshots** of its own state, as well as restore its state from snapshots when needed.
    2. The **Memento** is a **value object** that acts as a snapshot of the originator’s state. It’s a common practice to make the memento immutable and pass it the data only once, via the constructor.
    3. The **Caretaker** knows not only “when” and “why” to capture the **originator’s state**, but also when the state should be restored.
        
        A caretaker can **keep track** of the **originator’s history** by storing a stack of mementos. When the originator has to travel back in history, the caretaker fetches the **topmost memento** from the **stack** and passes it to the **originator’s restoration method**.
        
    4. In this implementation, the memento class is nested inside the originator. This lets the originator access the fields and methods of the memento, even though they’re declared private. On the other hand, the caretaker has very limited access to the memento’s fields and methods, which lets it store mementos in a stack but not tamper with their state.

**✍️ How to use it? ✍️**

- **How to Implement**
    1. Determine **what class** will **play** the role of the **originator**. It’s important to know whether the program **uses one central object** of this type or multiple smaller ones.
    2. Create the **memento class**. One by one, declare a set of fields that **mirror the fields** declared inside the **originator class**.
    3. Make the **memento** class **immutable**. A memento should accept the data just once, via the constructor. The **class should have no setters**.
    4. If your programming language supports nested classes, **nest the memento inside the originator**. If not, extract a blank interface from the memento class and make all other objects use it to refer to the memento. You may add some metadata operations to the interface, but nothing that exposes the originator’s state.
    5. Add a **method** for **producing mementos** to the **originator class**. The originator should pass its state to the memento via one or multiple arguments of the memento’s constructor.
        
        The return type of the method should be of the **interface** you extracted in the previous step (assuming that you extracted it at all). Under the hood, the memento-producing method should work **directly with** the **memento class.**
        
    6. Add a **method** for **restoring** the **originator’s state** **to its class**. It should **accept** a **memento object** as an **argument**. If you extracted an interface in the previous step, make it the type of the parameter. In this case, you need to typecast the incoming object to the memento class, since the originator needs full access to that object.
    7. The **caretaker**, whether it **represents a command object**, a **history**, or something entirely different, should know **when** to **request new mementos** from the **originator**, how to **store them** and **when to restore** the **originator** with a particular memento.
    8. The **link** between **caretakers** and **originators** may be moved into the **memento class**. In this case, each memento must be connected to the originator that had created it. The restoration method would also move to the memento class. However, this would all make sense only if the memento class is nested into originator or the originator class provides sufficient setters for overriding its state.
- The Memento’s principle **can be achieved** using **serialization**, which is quite common in Python. While it’s not the only and the most efficient way to make snapshots of an object’s state, it still allows storing state backups while protecting the originator’s structure from other objects.

**👍 Advantages 👍**

- You can produce snapshots of the object’s state **without violating its encapsulation**.
- You can **simplify the originator’s code** by letting the **caretaker maintain the history** of the originator’s state.

**👎 Disadvantages 👎**

- The app might consume **lots of RAM** if clients create mementos too often.
- **Caretakers should track the originator’s lifecycle** to be able to **destroy obsolete mementos**.
- Most dynamic programming languages, such as PHP, **Python** and JavaScript, **can’t guarantee that the state within the memento stays untouched**.

**↔️ Alternatives ↔️**

- Sometimes **Prototype** can be a **simpler alternative** to Memento. This works if the object, the state of which you want to store in the history, is fairly straightforward and doesn’t have links to external resources, or the links are easy to re-establish.

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- indispensable when dealing with **transactions** (i.e., if you need to roll back an operation on error).

**🛑 Worst practices 🛑**

- 

Sources:

[Memento](https://refactoring.guru/design-patterns/memento)

### **Observer**

**🔽 What? 🔽**

- behavioral design pattern

**🔁 What does it do? 🔁**

- allows some objects to notify other objects about changes in their state.

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- to define a **subscription mechanism** to notify multiple objects about any events that happen to the object they’re observing.
- when **changes to the state of one object** may **require changing other objects**, and the actual **set of objects** is **unknown beforehand** or **changes dynamically**. You can often experience this problem when working with classes of the graphical user interface. For example, you created custom button classes, and you want to let the clients hook some custom code to your buttons so that it fires whenever a user presses a button. You can add the subscription mechanism to your buttons, letting the clients hook up their custom code via custom subscriber classes.
- when **some objects** in your app **must observe others**, but only for a limited time or in **specific cases**. The subscription list is dynamic, so subscribers can join or leave the list whenever they need to.

🤔 **How does it work?** 🤔

- The object that **has some interesting** **state** is often called **subject**, but since it’s also going to **notify** other objects about the changes to its state, we’ll call it **publisher**. All other objects that **want to track changes** to the **publisher’s state** are called **subscribers**.
- The Observer pattern suggests that you add a **subscription mechanism** to the publisher class so individual objects can **subscribe** to or **unsubscribe** from a **stream of events** coming from that publisher. In reality, this mechanism consists of 1) an **array field** for **storing** a list of **references** to **subscriber objects** and 2) several **public methods** which allow **adding** subscribers **to** and **removing** them from that list. Now, whenever an **important event happens** to the publisher, it goes over its subscribers and **calls the specific notification method** on their objects.
- Pattern Structure Flow
    1. The **Publisher** issues events of interest to other objects. These events occur **when** the publisher **changes** its **state** or **executes** some **behaviors**. Publishers contain a **subscription infrastructure** that lets **new** subscribers **join** and **current** subscribers **leave** the list.
    2. When a new event happens, the **publisher goes** over the **subscription list** and **calls** the **notification method** declared in the **subscriber interface** on each subscriber object.
    3. The **Subscriber** **interface** declares the notification interface. In most cases, it consists of a single `update` method. The method may have several parameters that let the publisher pass some event details along with the update.
    4. **Concrete Subscribers** perform some actions in response to notifications issued by the publisher. All of these classes must implement the same interface so the publisher isn’t coupled to concrete classes.
    5. Usually, **subscribers need** some **contextual information** to handle the update correctly. For this reason, **publishers** often **pass** some **context data** as **arguments** of the **notification method**. The publisher can pass itself as an argument, letting subscriber fetch any required data directly.
    6. The **Client** creates **publisher** and **subscriber objects** separately and then **registers subscribers** for **publisher** updates.

- The difference between **Mediator** and **Observer** is often elusive. In most cases, you can implement either of these patterns; but sometimes you can apply both simultaneously. Let’s see how we can do that.
    - The primary goal of **Mediator** is to **eliminate mutual dependencies** among a set of system components. Instead, these components become dependent on a single mediator object.
    - The goal of Observer is to establish dynamic **one-way connections between objects**, where some objects act as subordinates of others.
- There’s a popular implementation of the **Mediator** pattern that relies on **Observer**. The **mediator** object plays the role of **publisher**, and the **components** act as **subscribers** which subscribe to and unsubscribe from the mediator’s events. When Mediator is implemented this way, it may look very similar to Observer.
- When you’re confused, remember that you can implement the Mediator pattern in other ways. For example, you can permanently link all the components to the same mediator object. This implementation won’t resemble Observer but will still be an instance of the Mediator pattern.
Now imagine a program where all components have become publishers, allowing dynamic connections between each other. There **won’t be a centralized mediator** object, only a **distributed set of observers**.

**✍️ How to use it? ✍️**

- **How to Implement**
    1. Look over your business logic and try to break it down into two parts: the **core** functionality, **independent from other code**, will act as the **publisher**; the **rest** will turn into a **set of** **subscriber** classes.
    2. Declare the **subscriber interface**. At a bare minimum, it should declare a single **`update`** method.
    3. Declare the **publisher interface** and describe a pair of methods for **adding** a **subscriber** object to and **removing** it from the list. Remember that publishers must work with subscribers only via the **subscriber interface**.
    4. Decide where to put the actual **subscription list** and the implementation of subscription methods. Usually, this code looks the same for all types of publishers, so the obvious place to put it is in an **abstract class** derived directly from the **publisher interface**. **Concrete publishers** extend that class, inheriting the subscription behavior.
        
        However, if you’re applying the pattern to an existing class hierarchy, consider an approach based on **composition**: put the **subscription logic** into a **separate object**, and make all real publishers use it.
        
    5. Create **concrete publisher classes**. Each time something important happens inside a publisher, it must **notify** all its subscribers.
    6. Implement the **update notification methods** in **concrete subscriber classes**. Most subscribers would need some context data about the event. It can be passed as an argument of the **notification method**.
        
        But there’s another option. Upon receiving a notification, the subscriber can **fetch** any **data** directly **from** the **notification**. In this case, the **publisher** must **pass itself** via the **update method**. The less flexible option is to link a publisher to the subscriber permanently via the constructor.
        
    7. The **client** must create all necessary **subscribers** and **register** them with proper **publishers**.

**👍 Advantages 👍**

- **Open/Closed Principle**. You can introduce new subscriber classes without having to change the publisher’s code (and vice versa if there’s a publisher interface).
- You can establish relations between objects at runtime.

**👎 Disadvantages 👎**

- Subscribers are notified in **random order**.

**↔️ Alternatives ↔️**

- 

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- 

**🛑 Worst practices 🛑**

- 

Sources:

[Observer](https://refactoring.guru/design-patterns/observer)

### **Mediator**

**🔽 What? 🔽**

- behavioral design pattern

**🔁 What does it do? 🔁**

- **restricts direct communications** between the objects and forces them to collaborate only via a **mediator object**.

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- to reduce **chaotic dependencies** between objects.
- when it’s **hard to change** some of the **classes** because they are tightly coupled to a bunch of other classes. The pattern lets you extract all the relationships between classes into a **separate class**, isolating any changes to a specific component from the rest of the components.
- when you can’t **reuse a component** in a **different program** because it’s **too dependent on other components**. After you apply the Mediator, individual components become unaware of the other components. They could still communicate with each other, albeit indirectly, through a mediator object. **To reuse a component** in a **different app**, you need to provide it with a **new mediator class**.
- when you find yourself creating **tons of component subclasses** just to reuse some **basic behavior** in various contexts. Since all relations between components are contained within the mediator, it’s easy to define entirely new ways for these components to collaborate by introducing new mediator classes, without having to change the components themselves.

🤔 **How does it work?** 🤔

- Pattern Structure Flow
    1. **Components** are various classes that **contain some business logic**. Each component has a **reference to a mediator**, declared with the type of the **mediator interface**. The component isn’t aware of the actual class of the mediator, so you can reuse the component in other programs by linking it to a different mediator.
    2. The **Mediator** **interface** declares methods of communication with **components**, which usually include just a single **notification method**. Components may pass any context as **arguments** of this method, including their own objects, but only in such a way that no coupling occurs between a receiving component and the sender’s class.
        1. **Concrete Mediator**s **encapsulate relations** between various components. Concrete mediators often keep references to **all components** they manage and sometimes even manage **their lifecycle**.
    3. **Components** must not be aware of other components. If something important happens within or to a component, it must only **notify the mediator**. When the mediator receives the notification, it can easily **identify the sender**, which might be just enough to decide **what component** should **be triggered** in **return**.
        
        From a component’s perspective, it all looks like a total black box. The sender doesn’t know who’ll end up handling its request, and the receiver doesn’t know who sent the request in the first place.
        

**✍️ How to use it? ✍️**

- **How to Implement**
    1. Identify a **group** of tightly **coupled classes** which would benefit from being **more independent** (e.g., for easier maintenance or simpler reuse of these classes).
    2. Declare the **mediator interface** and describe the desired communication protocol between mediators and various components. In most cases, a **single method** for receiving **notifications** from components is sufficient.
        
        This interface is crucial when you want to reuse component classes in different contexts. As long as the component works with its mediator via the generic interface, you can link the component with a different implementation of the mediator.
        
    3. Implement the **concrete mediator class**. Consider storing references to **all components** inside the mediator. This way, you could call any component from the mediator’s methods.
    4. You can go even further and make the mediator **responsible** for the **creation and destruction** of component objects. After this, the mediator may resemble a **factory** or a **facade**.
    5. **Components** should store a **reference** to the **mediator** object. The connection is usually established in the component’s constructor, where a **mediator** object is **passed as an argument**.
    6. Change the **components’ code** so that they **call the mediator’s notification** method instead of **methods on other components**. Extract the code that involves calling other components into the mediator class. Execute this code whenever the mediator receives notifications from that component.

**👍 Advantages 👍**

- **Single Responsibility Principle**. You can extract the communications between various components into a **single place**, making it easier to comprehend and maintain.
- **Open/Closed Principle**. You can introduce new mediators without having to change the actual components.
- You can **reduce coupling** between various components of a program.
- You can **reuse** individual **components** more **easily**.

**👎 Disadvantages 👎**

- Over time a mediator can evolve into a **God Object**.

**↔️ Alternatives ↔️**

- The synonym of the Mediator is the **Controller part of MVC pattern**.

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- 

**🛑 Worst practices 🛑**

- 

Sources:

[Mediator](https://refactoring.guru/design-patterns/mediator)

### State

**🔽 What? 🔽**

- behavioral design pattern

**🔁 What does it do? 🔁**

- lets an object **alter its behavior** when its **internal state changes**. It appears as if the object changed its class.

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- to convert **massive `switch`-base state** machines into **objects**.
- when you have an **object that behaves differently depending on its current state**, the **number of states** is **enormous**, and the **state-specific code changes frequently**. The pattern suggests that you extract all state-specific code into a set of distinct classes. As a result, you can add new states or change existing ones independently of each other, reducing the maintenance cost.
- when you have a class **polluted** with **massive conditionals** that alter how the class behaves according to the current values of the class’s fields. The State pattern lets you extract branches of these conditionals into methods of corresponding state classes. While doing so, you can also clean temporary fields and helper methods involved in state-specific code out of your main class.
- when you have a **lot of duplicate code** across **similar states** and transitions of a condition-based state machine. The State pattern lets you compose hierarchies of state classes and **reduce duplication** by extracting common code into abstract base classes.

🤔 **How does it work?** 🤔

- Pattern Structure Flow
    1. **Context** stores a **reference** to **one** of the **concrete state objects** and **delegates** to it all state-specific work. The context communicates with the state object via the **state interface**. The context exposes a setter for passing it a new state object.
    2. The **State** **interface** declares the state-specific methods. These methods should make sense for **all concrete states** because you don’t want some of your states to have useless methods that will never be called.
        1. **Concrete States** provide their own implementations for the state-specific methods. To avoid duplication of similar code across multiple states, you may provide intermediate abstract classes that encapsulate some common behavior.
        State objects may store a backreference to the **context** object. Through this reference, the state can fetch any required info from the context object, as well as initiate state transitions.
    3. Both **context** and **concrete states** can set the next state of the context and perform the actual state transition by replacing the state object linked to the context.

- Structure of **State pattern** may look similar to the **Strategy** pattern, but there’s one key difference. In the State pattern, the **particular states may** be **aware of each other** and initiate transitions from one state to another, whereas **strategies** almost **never know about** each **other**.

**✍️ How to use it? ✍️**

- **How to Implement**
    1. Decide what class will act as the **context**. It could be an existing class which already has the **state-dependent code**; or a new class, if the **state-specific code** is **distributed** across **multiple classes**.
    2. Declare the **state interface**. Although it may **mirror all** the **methods** declared **in the context**, aim only for those that may contain state-specific behavior.
        1. For every actual **state**, create a **class** that derives from the **state interface**. Then go over the methods of the context and extract all code related to that state into your newly created class.
            
            While moving the code to the state class, you might discover that it depends on private members of the context. There are several workarounds:
            
            - Make these fields or methods public.
            - Turn the behavior you’re extracting into a public method in the context and call it from the state class. This way is ugly but quick, and you can always fix it later.
            - Nest the state classes into the context class, but only if your programming language supports nesting classes.
    3. In the context class, add a **reference field** of the **state interface** type and a **public setter** that allows **overriding the value of that field**.
    4. Go over the method of the context again and **replace empty state conditionals** with **calls** to **corresponding methods** of the **state object**.
    5. To switch the state of the context, create an **instance** of one of the **state classes** and pass it to the context. You can do this within the context itself, or in various states, or in the client. Wherever this is done, the class becomes dependent on the concrete state class that it instantiates.

**👍 Advantages 👍**

- **Single Responsibility Principle**. Organize the code related to particular states into separate classes.
- **Open/Closed Principle**. Introduce new states without changing existing state classes or the context.
- **Simplify the code** of the context by **eliminating bulky** state machine conditionals.

**👎 Disadvantages 👎**

- Applying the pattern can be **overkill** if a state machine has **only a few states** or rarely changes.

**↔️ Alternatives ↔️**

- 

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- 

**🛑 Worst practices 🛑**

- 

Sources:

[State](https://refactoring.guru/design-patterns/state)

### **Strategy**

**🔽 What? 🔽**

- behavioral design pattern

**🔁 What does it do? 🔁**

- 

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- to define a **family of algorithms**, put each of them into a separate class, and make their **objects interchangeable**.
- when you want to use **different variants** of an **algorithm** within an object and **be able** to **switch** from **one algorithm to another** during runtime. The Strategy pattern lets you indirectly alter the object’s behavior at runtime by associating it with different sub-objects which can perform specific sub-tasks in different ways.
- when you have a lot of **similar classes** that only differ in the way they **execute some behavior**. The Strategy pattern lets you extract the varying behavior into a separate class hierarchy and combine the original classes into one, thereby reducing duplicate code.
- to **isolate the business logic** of a class from the **implementation details** of algorithms that may not be as important in the context of that logic. The Strategy pattern lets you isolate the code, internal data, and dependencies of various algorithms from the rest of the code. Various clients get a **simple interface** to execute the algorithms and switch them at runtime.
- when your class has a **massive conditional statement** that switches between **different variants** of the **same algorithm**. The Strategy pattern lets you do away with such a conditional by extracting all algorithms into separate classes, all of which implement the same interface. The original object delegates execution to one of these objects, instead of implementing all variants of the algorithm.

🤔 **How does it work?** 🤔

- Pattern Structure Flow
    1. The **Context** maintains a **reference** to one of the **concrete strategies** and communicates with this object only via the strategy interface.
    2. The **Strategy** **interface** is common to **all concrete strategies**. It declares a **method** the context uses **to execute a strategy**.
        1. **Concrete Strategies** implement different variations of an algorithm the context uses.
    3. The **context** calls the **execution method** on the linked strategy object each time it needs to **run** the **algorithm**. The context doesn’t know what type of strategy it works with or how the algorithm is executed.
    4. The **Client** **creates** a specific **strategy object** and passes it to the context. The context exposes a setter which lets clients replace the strategy associated with the context at runtime.

**✍️ How to use it? ✍️**

- **How to Implement**
    1. In the **context class**, identify an algorithm that’s prone to **frequent changes**. It may also be a **massive conditional** that selects and executes a variant of the same algorithm at runtime.
    2. Declare the **strategy interface** common to all variants of the algorithm.
    3. One by one, extract all algorithms into their own classes. They should all implement the **strategy interface**.
    4. In the **context class**, add a field for **storing a reference** to a **strategy object**. Provide a **setter** for **replacing values** of **that field**. The context should work with the strategy object only via the strategy interface. The context may define an interface which lets the strategy access its data.
    5. **Clients** of the context must associate it with a suitable strategy that matches the way they expect the context to perform its primary job.
- **Bridge, State, Strategy** (and to some degree **Adapter**) have very similar structures. Indeed, all of these patterns are based on **composition**, which is **delegating** work **to other objects**. However, they all solve different problems. A pattern isn’t just a recipe for structuring your code in a specific way. It can also communicate to other developers the problem the pattern solves.
- **Command** and **Strategy** may look similar because you can use both to **parameterize** an object with some action. However, they have very different intents.
    - You can use **Command** to convert any **operation** into an **object**. The operation’s parameters become fields of that object. The conversion lets you defer execution of the operation, queue it, store the history of commands, send commands to remote services, etc.
    - On the other hand, **Strategy** usually **describes different ways** of **doing** the **same thing**, letting you swap these algorithms within a single context class.
- **Decorator** lets you change the **skin** of an object, while **Strategy** lets you change the **guts**.
- **State** can be considered as an **extension of Strategy**. Both patterns are based on **composition**: they change the behavior of the context by delegating some work to helper objects. Strategy makes these objects completely independent and unaware of each other. However, **State** does**n’t restrict dependencies** between **concrete states**, letting them alter the state of the context at will.

**👍 Advantages 👍**

- You can **swap algorithms used inside** an object at runtime.
- You can **isolate** the **implementation details** of an algorithm from the code that uses it.
- You can replace **inheritance with composition**.
- **Open/Closed Principle**. You can introduce new strategies without having to change the context.

**👎 Disadvantages 👎**

- If you only have a couple of **algorithms** and they **rarely change**, there’s no real reason to overcomplicate the program with new classes and interfaces that come along with the pattern.
- **Clients must be aware** of the **differences between strategies** to be **able to select a proper one**.
- A lot of modern programming languages have functional type support that lets you implement different versions of an algorithm inside a set of anonymous functions. Then you could use these functions exactly as you’d have used the strategy objects, but without bloating your code with extra classes and interfaces.

**↔️ Alternatives ↔️**

- 

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- 

**🛑 Worst practices 🛑**

- 

Sources:

[Strategy](https://refactoring.guru/design-patterns/strategy)

### **Template Method**

**🔽 What? 🔽**

- behavioral design pattern

**🔁 What does it do? 🔁**

- defines the **skeleton** of an **algorithm** in the superclass but lets subclasses override specific steps of the algorithm without changing its structure.

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- when you want to let clients **extend only particular steps** of an **algorithm**, but **not the whole algorithm** or its structure. The Template Method lets you turn a monolithic algorithm into a **series of individual steps** which can be easily extended by subclasses while keeping intact the structure defined in a superclass.
- when you have **several classes** that contain **almost identical algorithms** with some minor differences. As a result, you might need to modify all classes when the algorithm changes. When you turn such an algorithm into a template method, you can also pull up the steps with similar implementations into a superclass, eliminating code duplication. Code that varies between subclasses can remain in subclasses.

🤔 **How does it work?** 🤔

- Pattern Structure Flow
    1. The **Abstract Class** declares methods that act as steps of an algorithm, as well as the actual template method which calls these methods in a **specific order**. The steps may either be declared `abstract` or have some default implementation.
    2. **Concrete Classes** can **override** all of the steps, but not the template method itself.
        
        ![image.png](OOP/image%2010.png)
        
- **Factory Method** is a specialization of Template Method. At the same time, a Factory Method may serve **as a step** in a **large Template Method**.
- Template Method is based on **inheritance**: it lets you alter parts of an algorithm by **extending** those parts in **subclasses**. **Strategy** is based on **composition**: you can alter parts of the object’s behavior by supplying it with different strategies that correspond to that behavior. **Template Method** works at the **class** level, so it’s **static**. **Strategy** works on the **object** level, **letting you switch behaviors** at runtime.

**✍️ How to use it? ✍️**

- **How to Implement**
    1. Analyze the **target algorithm** to see whether you can break it into steps. Consider which steps **are common to all subclasses** and which ones will **always be unique**.
    2. Create the **abstract base class** and declare the **template method** and a **set of abstract methods** representing the **algorithm’s steps**. Outline the algorithm’s structure in the template method by executing corresponding steps. Consider making the template method `final` to prevent subclasses from overriding it.
    3. It’s **okay if all the steps end up being abstract**. However, some steps might benefit from having a default implementation. Subclasses don’t have to implement those methods.
    4. Think of adding **hooks** between the crucial steps of the algorithm.
    5. For **each variation of the algorithm**, create a new **concrete subclass**. It ***must*** implement all of the abstract steps, but ***may*** also override some of the **optional ones**.

**👍 Advantages 👍**

- You can let clients override **only certain parts** of a **large algorithm**, making them less affected by changes that happen to other parts of the algorithm.
- You can **pull the duplicate code** into a **superclass**.

**👎 Disadvantages 👎**

- Some **clients** may be **limited** by the provided skeleton of an algorithm.
- You might violate the **Liskov Substitution Principle** by suppressing a default step implementation via a subclass.
- Template methods ****tend to be **harder to maintain** the **more steps** they have.

**↔️ Alternatives ↔️**

- 

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- 

**🛑 Worst practices 🛑**

- 

Sources:

[Template Method](https://refactoring.guru/design-patterns/template-method)

### Visitor

**🔽 What? 🔽**

- behavioral design pattern

**🔁 What does it do? 🔁**

- 

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- to separate algorithms from the objects on which they operate.
- when you need to perform an operation on all elements of a complex object structure (for example, an object tree). The Visitor pattern lets you execute an operation over a **set of objects** with **different classes** by having a visitor object implement several variants of the same operation, which correspond to all target classes.
- to clean up the business logic of auxiliary behaviors. The pattern lets you make the **primary classes** of your app **more focused on their main jobs** by **extracting** all other behaviors into a **set of visitor classes**.
- when a **behavior makes sense** only in **some classes** of a class hierarchy, but **not in others**. You can extract this behavior into a separate visitor class and implement only those visiting methods that accept objects of relevant classes, leaving the rest empty.

🤔 **How does it work?** 🤔

- Pattern Structure Flow
    1. The **Visitor** interface declares a **set of visiting methods** that can take **concrete elements** of an object structure as **arguments**. These methods may have the **same names** if the program is written in a language that supports **overloading**, but the type of their parameters must be different.
        1. Each **Concrete Visitor** implements several versions of the same behaviors, tailored for different concrete element classes.
    2. The **Element** interface declares a **method** for “**accepting**” visitors. This method should have one parameter declared with the type of the visitor interface.
        1. Each **Concrete Element** must implement the acceptance method. The purpose of this method is to redirect the call to the proper visitor’s method corresponding to the current element class. Be aware that even if a base element class implements this method, all subclasses must still override this method in their own classes and call the appropriate method on the visitor object.
    3. The **Client** usually represents a collection or some other complex object (for example, a **Composite** tree). Usually, clients aren’t aware of all the concrete element classes because they work with objects from that collection via some abstract interface.

**✍️ How to use it? ✍️**

- **How to Implement**
    1. Declare the **visitor interface** with a set of “**visiting” methods**, one per each **concrete element** class that exists in the program.
    2. Declare the **element interface**. If you’re working with an existing element class hierarchy, add the **abstract “acceptance” method** to the **base class** of the hierarchy. This method should **accept** a **visitor object** as an **argument**.
    3. Implement the **acceptance methods** in **all concrete element** classes. These methods must **simply redirect the call** to a **visiting method** on the incoming visitor object which matches the class of the current element.
    4. The **element classes** should only **work with visitors** via the **visitor interface**. **Visitors**, however, must be aware of all **concrete element classes**, referenced as parameter types of the visiting methods.
    5. For each behavior that can’t be implemented inside the element hierarchy, **create** a **new concrete visitor class** and implement all of the **visiting methods**.
        
        You might encounter a situation where the visitor will need access to some private members of the element class. In this case, you can either **make these fields or methods public**, violating the **element’s encapsulation**, or nest the visitor class in the element class. The latter is only possible if you’re lucky to work with a programming language that supports nested classes.
        
    6. The **client** must create **visitor objects** and pass them into elements via “acceptance” methods.
- You can treat Visitor as a powerful version of the **Command** pattern. Its objects can execute operations over various objects of different classes.
- You can use **Visitor** to execute an operation **over an entire Composite tree**.
- You can use Visitor along with **Iterator** to traverse a complex data structure and execute some operation over its elements, even if they all have different classes.

**👍 Advantages 👍**

- **Open/Closed Principle**. You can introduce a new behavior that can work with objects of different classes **without changing these classes**.
- **Single Responsibility Principle**. You can **move multiple versions** of the **same behavior** in**to** the **same class**.
- A visitor object can accumulate some useful information while working with various objects. This might be handy when you want to traverse some complex object structure, such as an object tree, and apply the visitor to each object of this structure.

**👎 Disadvantages 👎**

- You need to **update all visitors each time** a **class gets added** to or **removed** from the element hierarchy.
- Visitors might **lack** the **necessary access** to the **private fields** and **methods** of the elements that they’re **supposed to work with**.

**↔️ Alternatives ↔️**

- 

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- 

**🛑 Worst practices 🛑**

- 

Sources:

[Visitor and Double Dispatch](https://refactoring.guru/design-patterns/visitor-double-dispatch)

[Visitor](https://refactoring.guru/design-patterns/visitor)

# SOLID

**🔽 What? 🔽**

- five principles of Object-Oriented class design

**🔁 What does it do? 🔁**

- is a guide how you **split responsibilities, add features without risky modifications, respect subtype contracts, keep interfaces focused, and depend on abstractions**.
- Principles
    - The Single Responsibility Principle
    - The Open-Closed Principle
    - The Liskov Substitution Principle
    - The Interface Segregation Principle
    - The Dependency Inversion Principle

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- to make software more understandable, flexible, and maintatinable
- To create readable, and testable code that many developers can collaboratively work on.

🤔 **How does it work?** 🤔

- 

**✍️ How to use it? ✍️**

- 

**👍 Advantages 👍**

- 

**👎 Disadvantages 👎**

- 

**↔️ Alternatives ↔️**

- 

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- 

**🛑 Worst practices 🛑**

- 

Sources:

[SOLID Design Principles: Improve Object-Oriented Code in Python – Real Python](https://realpython.com/solid-principles-python/)

[The SOLID Principles of Object-Oriented Programming Explained in Plain English](https://www.freecodecamp.org/news/solid-principles-explained-in-plain-english/#:~:text=The%20SOLID%20Principles%20are%20five,and%20software%20architecture%20in%20general)

## **The Single Responsibility Principle**

**🔽 What? 🔽**

- Principle of SOLID

**🔁 What does it do? 🔁**

- states that a **class** should **do one thing** and therefore it should have **only a single reason to change**

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- 

🤔 **How does it work?** 🤔

- 

**✍️ How to use it? ✍️**

- You define an **abstract interface** that subclasses extend without forcing edits to the existing class.

**👍 Advantages 👍**

- 

**👎 Disadvantages 👎**

- 

**↔️ Alternatives ↔️**

- 

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- File manager that involves reading and writing with ZIP compressing and decompressing
    
    ```python
    from pathlib import Path
    from zipfile import ZipFile
    
    class FileManager:
        def __init__(self, filename):
            self.path = Path(filename)
    
        def read(self, encoding="utf-8"):
            return self.path.read_text(encoding)
    
        def write(self, data, encoding="utf-8"):
            self.path.write_text(data, encoding)
    
        def compress(self):
            with ZipFile(self.path.with_suffix(".zip"), mode="w") as archive:
                archive.write(self.path)
    
        def decompress(self):
            with ZipFile(self.path.with_suffix(".zip"), mode="r") as archive:
                archive.extractall()
    ```
    
    ```python
    from pathlib import Path
    from zipfile import ZipFile
    
    class FileManager:
        def __init__(self, filename):
            self.path = Path(filename)
    
        def read(self, encoding="utf-8"):
            return self.path.read_text(encoding)
    
        def write(self, data, encoding="utf-8"):
            self.path.write_text(data, encoding)
    
    class ZipFileManager:
        def __init__(self, filename):
            self.path = Path(filename)
    
        def compress(self):
            with ZipFile(self.path.with_suffix(".zip"), mode="w") as archive:
                archive.write(self.path)
    
        def decompress(self):
            with ZipFile(self.path.with_suffix(".zip"), mode="r") as archive:
                archive.extractall()
    ```
    
- 

**🛑 Worst practices 🛑**

- common mistake to mix **persistence** logic with **business** logic.

Sources:

[SOLID Design Principles: Improve Object-Oriented Code in Python – Real Python](https://realpython.com/solid-principles-python/)

## Open-Closed Principle

**🔽 What? 🔽**

- requires that classes should be **open for extension** and **closed to modification**

**🔁 What does it do? 🔁**

- 

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- **Modification** means changing the code of an existing **class**, and **extension** means **adding** new functionality.

🤔 **How does it work?** 🤔

- class should have **only one responsibility**, as expressed through its **methods**.

**✍️ How to use it? ✍️**

- 

**👍 Advantages 👍**

- 

**👎 Disadvantages 👎**

- 

**↔️ Alternatives ↔️**

- 

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- If a class takes care of **more than one task**, then you should separate those tasks into dedicated classes with descriptive names
- From validation the shape type for area calculation to
    
    ```python
    from math import pi
    
    class Shape:
        def __init__(self, shape_type, **kwargs):
            self.shape_type = shape_type
            if self.shape_type == "rectangle":
                self.width = kwargs["width"]
                self.height = kwargs["height"]
            elif self.shape_type == "circle":
                self.radius = kwargs["radius"]
            else:
                raise TypeError("Unsupported shape type")
    
        def calculate_area(self):
            if self.shape_type == "rectangle":
                return self.width * self.height
            elif self.shape_type == "circle":
                return pi * self.radius**2
            else:
                raise TypeError("Unsupported shape type")
    ```
    
    ```python
    from abc import ABC, abstractmethod
    from math import pi
    
    class Shape(ABC):
        def __init__(self, shape_type):
            self.shape_type = shape_type
    
        @abstractmethod
        def calculate_area(self):
            pass
    
    class Circle(Shape):
        def __init__(self, radius):
            super().__init__("circle")
            self.radius = radius
    
        def calculate_area(self):
            return pi * self.radius**2
    
    class Rectangle(Shape):
        def __init__(self, width, height):
            super().__init__("rectangle")
            self.width = width
            self.height = height
    
        def calculate_area(self):
            return self.width * self.height
    
    class Square(Shape):
        def __init__(self, side):
            super().__init__("square")
            self.side = side
    
        def calculate_area(self):
            return self.side**2
    ```
    

**🛑 Worst practices 🛑**

- 

Sources:

## Liskov Substitution Principle

**🔽 What? 🔽**

- 

**🔁 What does it do? 🔁**

- introduced by [Barbara Liskov](https://en.wikipedia.org/wiki/Barbara_Liskov) in a 1987
- ensures that a class and its derived classes are interchangeable without modifying the program’s expected outcomes.

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- Ensures your codebase remains **robust, flexible**, and **maintainable**, significantly **reducing** the likelihood of **bugs** and making **future expansions easier** to implement.

🤔 **How does it work?** 🤔

- objects of a superclass should be replaceable with objects of a subclass without affecting the correctness of the program.
- subclasses should **extend the base classes without changing their behavior**

**✍️ How to use it? ✍️**

**👍 Advantages 👍**

- 

**👎 Disadvantages 👎**

- 

**↔️ Alternatives ↔️**

- 

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- While a square is a **specific type** of rectangle in mathematics, the classes that represent those shapes **shouldn’t inherit from each other** via a parent-child relationship if you want them to abide by the LSP. The rectangle and square classes have different behavior in the OOP. From overusing the inheritance behavior of the Square subclass of the Rectangle class to a squarer as a sibling class to Recatngle as children classes of Shape class.
    
    ```python
    from abc import ABC, abstractmethod
    
    class Shape(ABC):
        @abstractmethod
        def calculate_area(self):
            pass
    
    class Rectangle(Shape):
        def __init__(self, width, height):
            self.width = width
            self.height = height
    
        def calculate_area(self):
            return self.width * self.height
            
    class Square(Rectangle):
        def __init__(self, side):
            super().__init__(side, side)
    
        def __setattr__(self, key, value):
            super().__setattr__(key, value)
            if key in ("width", "height"):
                self.__dict__["width"] = value
                self.__dict__["height"] = value
    ```
    
    ```python
    from abc import ABC, abstractmethod
    
    class Shape(ABC):
        @abstractmethod
        def calculate_area(self):
            pass
    
    class Rectangle(Shape):
        def __init__(self, width, height):
            self.width = width
            self.height = height
    
        def calculate_area(self):
            return self.width * self.height
    
    class Square(Shape):
        def __init__(self, side):
            self.side = side
    
        def calculate_area(self):
            return self.side ** 2
    ```
    
- Example of interchangability. Here a polymorphism and abstraction are involved to use an abstract method for different shapes as they are Shape class, but not sublclasses
    
    ```python
    >>> from shapes_lsp import Rectangle, Square
    
    >>> def get_total_area(shapes):
    ...     return sum(shape.calculate_area() for shape in shapes)
    ...
    
    >>> get_total_area([Rectangle(10, 5), Square(5)])
    75
    ```
    

**🛑 Worst practices 🛑**

- 

Sources:

## **Interface Segregation Principle (ISP)**

**🔽 What? 🔽**

- 

**🔁 What does it do? 🔁**

- comes from the same mind as the **single-responsibility principle**

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- to create different machines with different sets of functionalities, making your design more **flexible and extensible**.

🤔 **How does it work?** 🤔

- Clients should not be forced to depend upon methods that they do not use. Interfaces belong to clients, not to hierarchies. **clients** are **classes and subclasses**, and **interfaces** consist of **methods and attributes**

**✍️ How to use it? ✍️**

- 

**👍 Advantages 👍**

- 

**👎 Disadvantages 👎**

- 

**↔️ Alternatives ↔️**

- 

**✅ Best practices ✅**

- if a class **doesn’t use** particular **methods or attributes,** then those methods and attributes should be **segregated** into more **specific classes**

**🛠️ Use cases 🛠️**

- From using an OldPrinter subclass of Printer abstract class to Interfaces Segregation to creating multiple inheritance for a NewPrinter
    
    ```python
    from abc import ABC, abstractmethod
    
    class Printer(ABC):
        @abstractmethod
        def print(self, document):
            pass
    
        @abstractmethod
        def fax(self, document):
            pass
    
        @abstractmethod
        def scan(self, document):
            pass
    
    class OldPrinter(Printer):
        def print(self, document):
            print(f"Printing {document} in black and white...")
    
        def fax(self, document):
            raise NotImplementedError("Fax functionality not supported")
    
        def scan(self, document):
            raise NotImplementedError("Scan functionality not supported")
    
    class ModernPrinter(Printer):
        def print(self, document):
            print(f"Printing {document} in color...")
    
        def fax(self, document):
            print(f"Faxing {document}...")
    
        def scan(self, document):
            print(f"Scanning {document}...")
    ```
    
    ```python
    from abc import ABC, abstractmethod
    
    class Printer(ABC):
        @abstractmethod
        def print(self, document):
            pass
    
    class Fax(ABC):
        @abstractmethod
        def fax(self, document):
            pass
    
    class Scanner(ABC):
        @abstractmethod
        def scan(self, document):
            pass
    
    class OldPrinter(Printer):
        def print(self, document):
            print(f"Printing {document} in black and white...")
    
    class NewPrinter(Printer, Fax, Scanner):
        def print(self, document):
            print(f"Printing {document} in color...")
    
        def fax(self, document):
            print(f"Faxing {document}...")
    
        def scan(self, document):
            print(f"Scanning {document}...")
    ```
    

**🛑 Worst practices 🛑**

- 

Sources:

## **Dependency Inversion Principle (DIP)**

**🔽 What? 🔽**

- 

**🔁 What does it do? 🔁**

- states that our **classes** should **depend** upon **interfaces** or abstract classes instead of **concrete classes and functions**.
- states that **high-level modules** should **not depend** on **low-level modules**, but both should depend on abstractions

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- to fix tight coupling

🤔 **How does it work?** 🤔

- 

**✍️ How to use it? ✍️**

- 

**👍 Advantages 👍**

- 

**👎 Disadvantages 👎**

- 

**↔️ Alternatives ↔️**

- 

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- From tight coupled relationship between Database, Backend and front end to make the front end more independent about a datasource which could send data to FrontEnd
    
    ```python
    class FrontEnd:
        def __init__(self, back_end: BackEnd):
            self.back_end = back_end
    
        def display_data(self):
            data = self.back_end.get_data_from_database()
            print("Display data:", data)
    
    class BackEnd:
        def get_data_from_database(self):
            return "Data from the database"
    ```
    
    ```python
    from abc import ABC, abstractmethod
    
    class FrontEnd:
        def __init__(self, data_source: DataSource):
            self.data_source = data_source
    
        def display_data(self):
            data = self.data_source.get_data()
            print("Display data:", data)
    
    class DataSource(ABC):
        @abstractmethod
        def get_data(self):
            pass
    
    class Database(DataSource):
        def get_data(self):
            return "Data from the database"
    
    class API(DataSource):
        def get_data(self):
            return "Data from the API"
    ```
    

**🛑 Worst practices 🛑**

- 

Sources:

[solid.python/5.dip.py at master · heykarimoff/solid.python](https://github.com/heykarimoff/solid.python/blob/master/5.dip.py)

# Special methods

**🔽 What? 🔽**

- Special (or **dunder**, or **magic**) methods are predefined built-in methods

**🔁 What does it do? 🔁**

- 

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- to **cutomize how** object **behave** with built-in operations (creation, printing, arithemtic, comparisons etc.)

🤔 **How does it work?** 🤔

- Python calls them automatically when need it, we don’t call them.

**✍️ How to use it? ✍️**

- 

**👍 Advantages 👍**

- 

**👎 Disadvantages 👎**

- 

**↔️ Alternatives ↔️**

- 

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- 

**🛑 Worst practices 🛑**

- 

Sources:

[Every dunder method in Python](https://www.pythonmorsels.com/every-dunder-method/)

## Object creation and initialization

- `__init__()` - (initializer or constructor) runs after object is created to initialize attributes. Fills it with data. The process of setting up the house (furnishing and decorating) is similar to the `__init__()` method.

```python
def __init__(self, owner, balance):
self.owner = owner
self.__balance = balance
```

- `__new__()` - runs before `__init__()` to actually create the object. **Rarely** used when you want to **control how** an object is created before it’s initialized, or when you **subclass immutable** types like `int, str, or tuple`. It has to return an instance to create it.
- `__del__()` - is used to do extra actions before thу object would be deleted with `del` keyword. `del` and `pop()` difference:
    
    ```python
    x = ["apple", "banana", "cherry"]
    del x[0]
    print(x)  # ['banana', 'cherry']
    
    fruit = x.pop(0)
    print(fruit)  # 'banana'
    print(x)      # ['cherry']
    ```
    

### `__init__()`

**🔽 What? 🔽**

- 

**🔁 What does it do? 🔁**

- 

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- 

🤔 **How does it work?** 🤔

- 

**✍️ How to use it? ✍️**

- 

**👍 Advantages 👍**

- 

**👎 Disadvantages 👎**

- 

**↔️ Alternatives ↔️**

- 

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- 

**🛑 Worst practices 🛑**

- turn their `__init__` method into a “God method,” filled with conditional logic and type checking to handle various input formats

Sources:

## Representation & conversion

- `__str__()` is called by  `print()` and `str()` built-in functions `__repr__()` is called to show the blueprint of the object (module, where the class is defined, class name and memory address in hexadecimal format) 
are responsible for represetation behaviour of the object as a string.
- `__format__()` - is used by `string.format()` as well as the `format()` built-in function. is used to create formatted strings
    
    ```python
    a = "shakshi" # name 
    b = 22 # age
    
    msg = "My name is {0} and I am {1} years old.".format(a,b)
    print(msg)
    ```
    
- `__bytes__()`

**🔽 What? 🔽**

- 

**🔁 What does it do? 🔁**

- 

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- 

🤔 **How does it work?** 🤔

- 

**✍️ How to use it? ✍️**

- 

**👍 Advantages 👍**

- 

**👎 Disadvantages 👎**

- 

**↔️ Alternatives ↔️**

- 

**✅ Best practices ✅**

- **Always** implement `__repr__()` for any class you develop, as it's a good development practice that **enhances the debuggability** of your code.
- Implement `__str__()` when you need a **user-friendly representation** of your object, especially if the object is meant to be used by **people** who may not be **interested** in its **internal workings** or how to recreate it.

**🛠️ Use cases 🛠️**

- 

**🛑 Worst practices 🛑**

- 

Sources:

### **`__bytes__()`**

**🔽 What? 🔽**

- 

**🔁 What does it do? 🔁**

- returns a bytes representation of an object
- can **serialize** more complex objects by combining multiple values into a structured binary format

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- 

🤔 **How does it work?** 🤔

- It's called by the built-in `bytes()` function
- it takes no parameters (except `self`), must return a bytes object. Unlike `__str__`, it focuses on **binary data** rather than **text**.

**✍️ How to use it? ✍️**

- 

**👍 Advantages 👍**

- 

**👎 Disadvantages 👎**

- 

**↔️ Alternatives ↔️**

- 

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- Serializing Complex Objects (e.g. network transmission or file storage)
    
    ```python
    import struct
    
    class Person:
        def __init__(self, name, age, height):
            self.name = name
            self.age = age
            self.height = height
        
        def __bytes__(self):
            name_bytes = self.name.encode('utf-8')
            return struct.pack(
                f'I{len(name_bytes)}sIf',
                len(name_bytes),
                name_bytes,
                self.age,
                self.height
            )
    
    person = Person("Alice", 30, 1.75)
    print(bytes(person))  # Binary representation
    ```
    
    This example uses the `struct` module to create a packed binary representation of a `Person` object.  `struct` module handles variable-length strings by including the length prefix. The format string `I{len(name_bytes)}sIf` specifies: unsigned int for `len`gth, bytes for `name`, unsigned int for `age`, and float for `height`. This creates a well-defined binary structure.
    
- **Network Protocol Implementation.** `__bytes__()` ****is particularly useful for implementing network protocols where objects need to be **converted** to specific binary formats for transmission.
    
    ```python
    class NetworkPacket:
        def __init__(self, packet_type, sequence, payload):
            self.packet_type = packet_type
            self.sequence = sequence
            self.payload = payload
        
        def __bytes__(self):
            header = bytes([
                self.packet_type,
                (self.sequence >> 8) & 0xFF,
                self.sequence & 0xFF,
                len(self.payload)
            ])
            return header + self.payload
    
    packet = NetworkPacket(1, 256, b'Hello')
    print(bytes(packet))  # b'\x01\x01\x00\x05Hello'
    ```
    
    This `NetworkPacket` class implements a simple protocol header followed by payload data. The header contains type, sequence number (as two bytes), and payload length.
    
    The `__bytes__` method carefully constructs the binary representation by packing the header fields and concatenating the payload. This format could be sent over a network connection.
    

**🛑 Worst practices 🛑**

- 

Sources:

[Python __bytes__ Method - Complete Guide](https://zetcode.com/python/dunder-bytes/)

## Comparison operators

- `__eq__()`, `__ne__()`,
    
    By default, the `__eq__` method for new class instances compares the **memory addresses** of the objects. This means that, unless overridden, two instances of a class will be considered equal **only** if they are **actually the same instance**.
    
- Code example:
    
    ```python
    class Item:
        def __init__(self, name):
            self.name = name
    
    item1 = Item('Apple')
    **item2** = Item('Apple')
    *item3* = item1
    
    print(item1 == **item2**)  
    # Output: False, because they are different instances
    print(item1 == *item3*)  
    # Output: True, because they are the same instance
    ```
    
    Overriding `__eq__()` allows us to define what exactly to compare the equality.
    
    ```python
    class Item:
        def __init__(self, name):
            self.name = name
    
        def __eq__(self, other):
            if not isinstance(other, Item):
                # Don't attempt to compare against unrelated types
                return NotImplemented
            **return self.name == other.name**
    
    item1 = Item('Apple')
    **item2** = Item('Apple')
    *item3* = Item('Banana')
    
    print(item1 == **item2**)  # Output: True, because their names are the same
    print(item1 == *item3*)  # Output: False, because their names are different
    ```
    
- `__lt__(), __le__(), __gt__(), __ge__()`
    
    The `functools.total_ordering` **decorator** allows you to implement just `__eq__` and one other comparison method (`__lt__`, `__le__`, `__gt__`, or `__ge__`). Once **applied**, `functools.total_ordering` will automatically generate the remaining comparison methods for you. This drastically reduces the amount of boilerplate code you need to write and maintain.
    
    - Code Example Usage
        
        ```python
        class Item:
            def __init__(self, name, value):
                self.name = name
                self.value = value
        
            def __eq__(self, other):
                return self.value == other.value
        
            def __ne__(self, other):
                return self.value != other.value
        
            def __lt__(self, other):
                return self.value < other.value
        
            def __le__(self, other):
                return self.value <= other.value
        
            def __gt__(self, other):
                return self.value > other.value
        
            def __ge__(self, other):
                return self.value >= other.value
        
        # Creating instances of Item
        item1 = Item('Apple', 10)
        item2 = Item('Banana', 20)
        
        # Comparing the items
        print(item1 == item2)  # Output: False
        print(item1 != item2)  # Output: True
        print(item1 < item2)   # Output: True
        print(item1 <= item2)  # Output: True
        print(item1 > item2)   # Output: False
        print(item1 >= item2)  # Output: False
        ```
        
    - `total_ordering` **decorator usage**
        
        ```python
        from functools import total_ordering
        
        @total_ordering
        class Item:
            def __init__(self, value):
                self.value = value
        
            def __eq__(self, other):
                return self.value == other.value
        
            def __lt__(self, other):
                return self.value < other.value
        
        # With the above setup, Item instances can be compared using any of the comparison operators.
        
        ```
        

**🔽 What? 🔽**

- 

**🔁 What does it do? 🔁**

- 

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- 

🤔 **How does it work?** 🤔

- 

**✍️ How to use it? ✍️**

- 

**👍 Advantages 👍**

- 

**👎 Disadvantages 👎**

- 

**↔️ Alternatives ↔️**

- 

**✅ Best practices ✅**

- **Type Checking**: Use `isinstance(other, ClassName)` to ensure that you're comparing objects of the **same type** or compatible types.
- **Handling Not Implemented**: Return `NotImplemented` if the comparison is attempted with an **unrelated type**. This allows Python to **handle the comparison** in other ways **rather than raising an error** immediately.
- **Consistency** with Other Comparison Methods: If you override **eq**, **consider overriding other** comparison methods (**ne**, **lt**, **le**, **gt**, **ge**) to **ensure consistent** behavior acros all types of comparisons.
- It’s often sufficient to implement `__eq__` and one of the ordering comparisons (`__lt__`, `__gt__`, etc.) because **the `functools.total_ordering`** decorator can fill in the rest.

**🛠️ Use cases 🛠️**

- These methods become especially powerful when working with **collections of objects**, allowing for **sorting** and **filtering** based on custom criteria.
- Implementing comparison operators can **enhance the readability** and **expressiveness** of your **code**, making operations involving your objects feel more **natural and intuitive**.

**🛑 Worst practices 🛑**

- 

Sources:

## Arythemtic & numeric operations

- `__add__()`, `__sub__()`, `__mul__()`, `__truediv__()`, `__floordiv__()`, `__mod__()`, `__pow__()`
- `__iadd__()`, `__isub__()`, `__imul__()`… - +=, -=
- `__neg__()`, `__pos__()`, `__abs__()`

## Item access (indexing, key-value) and container methods

- `__getitem__()`  is used when we use the indexing operator`[]` on an object.
- `__setitem__()`  when we update thу element of the array object.
    - Code Example Usage
        
        ```python
        class bank_record:
            
            def __init__(self, name):
                
                self.record = {
                                "name": name,
                                "balance": 100,
                                "transaction":[100]
                                }
        
            def __getitem__(self, key):
                
                return self.record[key]
        
            def __setitem__(self, key, newvalue):
                
                if key =="balance" and newvalue != None and newvalue>= 100:
                    self.record[key] += newvalue
                    
                elif key =="transaction" and newvalue != None:
                    self.record[key].append(newvalue)
            
            def getBalance(self):
                return self.__getitem__("balance")
        
            def updateBalance(self, new_balance):
                
                self.__setitem__("balance", new_balance)
                self.__setitem__("transaction", new_balance)    
            
            def getTransactions(self):
                return self.__getitem__("transaction")
        
            def numTransactions(self):
                return len(self.record["transaction"])
        
        sam = bank_record("Sam")
        print("The balance is : "+str(sam.getBalance()))
        
        sam.updateBalance(200)
        print("The new balance is : "+str(sam.getBalance()))
        print("The no. of transactions are: "+str(sam.numTransactions()))
        
        sam.updateBalance(300)
        print("The new balance is : "+str(sam.getBalance()))
        print("The no. of transactions are: "+str(sam.numTransactions()))
        print("The transaction history is: "+ str(sam.getTransactions()))
        
        """Output
        The balance is : 100
        The new balance is : 300
        The no. of transactions are: 2
        The new balance is : 600
        The no. of transactions are: 3
        The transaction history is: [100, 200, 300]"""
        ```
        
        In this version, implementing `__getitem__` allows you to use dictionary-like access such as `sam["balance"]`, which makes your object behave like a container; in the second version, that behavior is removed.
        
- `__delitem__()`, `__contains__()`

**🔽 What? 🔽**

- 

**🔁 What does it do? 🔁**

- 

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- 

🤔 **How does it work?** 🤔

- 

**✍️ How to use it? ✍️**

- 

**👍 Advantages 👍**

- 

**👎 Disadvantages 👎**

- 

**↔️ Alternatives ↔️**

- 

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- These methods are extremely useful in Data Science for working with custom data structures, such as data frames, matrices, or any container types that requirу specific access patterns.
    - getitem -
    - Accessing **specific rows or columns** in a data frame.
    - Retrieving elements from a **custom array or matrix** based on their **position**.
    - Implementing **slicing** operations to fetch ranges of data efficiently.
- setitiem
    - **Modify** specific **rows or columns** in a data frame.
    - **Change values** within a custom array or matrix.
    - Implement checks or **transformations when** data is **assigned**, ensuring data integrity.

**🛑 Worst practices 🛑**

- 

Sources:

## Iteration

- `__iter__()`  returns an iterator object itself, which contains `__next__()` function
    
    ```python
    class list_iterator:
        def __init__(self, lst):
            self._list = lst
            self._index = 0
    
        def __iter__(self):
            return self
    
        def __next__(self):
            if self._index >= len(self._list):
                raise StopIteration
            value = self._list[self._index]
            self._index += 1
            return value
    ```
    
- `__next__()`  returns the new value which we obtaion after computations in this method. It is a method of iterator object

## Attribute access & management

- `__getattr__()` – called when attribute not found
- `__setattr__()` – called on setting an attribute
- `__delattr__()` – called on deleting an attribute
- `__getattribute__()` – called on any attribute access

## Callable objects

- `__call__()` – make an object callable like a function

## Context managers

- `__enter__()` – start of `with` block
- `__exit__()` – end of `with` block

## Miscellaneous

- `__len__()` – length of object (`len()`)
- `__bool__()` – truth value testing (`bool()`)
- `__hash__()` – hash value (`hash()`)
- `__copy__()`, `__deepcopy__()` – for copying objects

Sources:  

[Special Methods in Python OOP](https://medium.com/data-bistrot/special-methods-in-python-oop-3b99585ee29c)

[__new__ in Python - GeeksforGeeks](https://www.geeksforgeeks.org/python/__new__-in-python/)

### **`hash()`**

**🔽 What? 🔽**

- Built-in function in Python

**🔁 What does it do? 🔁**

- returns an integer hash value for an object

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- 

🤔 **How does it work?** 🤔

- 

**✍️ How to use it? ✍️**

- Only immutable objects can be hashed
- Usage and explanation
    
    ```python
    print(hash(10))
    print(hash("python"))
    ```
    
    - hash(10) returns **10** because integers hash to themselves
    - hash("python") returns a **generated integer** based on the string content

**👍 Advantages 👍**

- 

**👎 Disadvantages 👎**

- 

**↔️ Alternatives ↔️**

- 

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- 

**🛑 Worst practices 🛑**

- 

Sources:

# Special attributes

**🔽 What? 🔽**

- 

**🔁 What does it do? 🔁**

- 

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- 

🤔 **How does it work?** 🤔

- 

**✍️ How to use it? ✍️**

- 

**👍 Advantages 👍**

- 

**👎 Disadvantages 👎**

- 

**↔️ Alternatives ↔️**

- 

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- 

**🛑 Worst practices 🛑**

- 

Sources:

[🔎 special attributes python - Google Search](https://www.google.com/search?q=special+attributes+python&sca_esv=f9e0460a4f421807&sxsrf=ANbL-n4GG2JEPtZgs5wjA-lRZVjR1xVoIg%3A1772781096388&ei=KH6qaYPAF_-Ixc8PzLe5qA0&biw=738&bih=673&ved=0ahUKEwiD9I6c3IqTAxV_RPEDHcxbDtUQ4dUDCBA&uact=5&oq=special+attributes+python&gs_lp=Egxnd3Mtd2l6LXNlcnAiGXNwZWNpYWwgYXR0cmlidXRlcyBweXRob24yBhAAGBYYHjIGEAAYFhgeMgUQABjvBTIFEAAY7wUyBRAAGO8FMgUQABjvBUj4FFDsAljYEnABeACQAQKYAacBoAHeB6oBAzAuN7gBA8gBAPgBAZgCBqACuAXCAgkQABiwAxgHGB7CAggQABiABBjLAZgDAIgGAZAGCpIHAzEuNaAHpyWyBwMwLjW4B7EFwgcHMC4xLjQuMcgHIYAIAA&sclient=gws-wiz-serp)

[Using Python's .__dict__ to Work With Attributes – Real Python](https://realpython.com/python-dict-attribute/)

# Getter and Setter

**🔽 What? 🔽**

- Getters(also known as 'accessors') and setters (aka. 'mutators')
- methods

**🔁 What does it do? 🔁**

- Pythonic way to introduce **attributes** is to make them **public**

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- to ensure the principle of data encapsulation
- *getter* for retrieving the data and the *setter* for changing the data

🤔 **How does it work?** 🤔

- 

**✍️ How to use it? ✍️**

- Basic example

**👍 Advantages 👍**

- 

**👎 Disadvantages 👎**

- 

**↔️ Alternatives ↔️**

- If you see a getter and setter that do nothing except get and set a member then this member should be a public member instead

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- **Dynamic Computation or Validation.** If getting or setting an attribute involves complex computations or validation that goes beyond simple attribute access, using getter and setter methods allows you to encapsulate this logic more explicitly.
    
    ```python
    class Circle:
        def __init__(self, radius):
            self._radius = radius
    
        def get_area(self):
            return 3.14 * self._radius**2
    
        def set_radius(self, value):
            if value < 0:
                raise ValueError("Radius must be non-negative")
            self._radius = value
    ```
    
- External **API Compatibility**: When working with external APIs or libraries that **expect traditional getter and setter methods**, adhering to their conventions may be necessary for compatibility. You may have a popular Java implementation of a class and you write a Python class which has to simulate the interface for example.
- **Additional Arguments** to Attributes: Let's consider an example with a `Person` class which has an attribute `height`, and the setter method `set_height()` includes additional logic to ensure that the height is within a valid range. The additional argument `validate` controls whether the validation should be performed:
    
    ```python
    class Person:
        def __init__(self, name, height):
            self.name = name
            self._height = height
    
        def get_height(self):
            return self._height
    
        def set_height(self, value, validate=True):
            if validate and not (150 <= value <= 200):
                raise ValueError("Height must be between 150 and 200 cm.")
            self._height = value
    
    # Example usage:
    person = Person("Alice", height=170)
    
    # Try setting height within the valid range
    person.set_height(175)
    print(person.get_height())  
    
    # Try setting height outside the valid range
    try:
        person.set_height(210)
    except ValueError as e:
        print(e)  
    
    person.set_height(210, validate=False) 
    print(person.get_height()) 
    ```
    

**🛑 Worst practices 🛑**

- Basic ugly example
    
    ```python
    class P:
    
        def __init__(self, x):
            self.__x = x
    
        def get_x(self):
            return self.__x
    
        def set_x(self, x):
            self.__x = x
    p1 = P(42)
    p2 = P(4711)
    p1.get_x() # 42
    
    p1.set_x(47)
    p1.set_x(p1.get_x()+p2.get_x()) # 47 + 4711
    p1.get_x() # 4758
    ```
    
- private members usually don't need getters and setters

Sources:

[3. Properties vs. Getters and Setters | OOP | python-course.eu](https://python-course.eu/oop/properties-vs-getters-and-setters.php)

# Descriptor

**🔽 What? 🔽**

- mechanism in Python language
- a way that events will happen when attributes are referenced in the model.
- a powerful, general purpose protocol

**🔁 What does it do? 🔁**

- to implement functions similar to `__private` variables in Python

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- to **customize** how **attribute access** works in classes
- to define how attributes are **retrieved, set, or deleted** by implementing specific methods

🤔 **How does it work?** 🤔

- Python will perform a certain translation of attribute access operations, and the method of this translation is determined by the descriptor protocol

**✍️ How to use it? ✍️**

- are defined at the class level
- `__get__ (self, obj, type=None)` — used to access attributes. It returns the value of the attribute. If the attribute is illegal, it can throw a corresponding exception like `ValueError`. If the attribute does not exist, it will report `AttributeError`. If your descriptor implements just `.__get__()`, then it’s said to be a **non-data descriptor.** If it implements `.__set__()` or `.__delete__()`, then it’s said to be a **data descriptor**.
- `__set__ (self, obj, value)`  — used to set the property’s values, `None` will be returned.
- `__delete__ (self, obj)`  — controls the deletion of attributes; `None` will be returned.
- `__set_name__(self, owner, name)`  —
- Basic example
    
    ```python
    class Temperature:
        def __init__(self, value=0):
            self._temperature = value
    
        def __get__(self, instance, owner):
            return self._temperature
    
        def __set__(self, instance, value):
            if value < -273.15:
                raise ValueError("Temperature below absolute zero is not possible")
            self._temperature = value
    
    class Thermometer:
        temperature = Temperature()
    
    ## Usage
    thermo = Thermometer()
    thermo.temperature = 25  ## Sets temperature
    print(thermo.temperature)  ## Retrieves temperature
    ```
    
- Advanced Descriptor Techniques
    
    ```python
    class ComputedDescriptor:
        def __init__(self, compute_func):
            self.compute_func = compute_func
            self._cache = {}
    
        def __get__(self, instance, owner):
            if instance is None:
                return self
    
            if instance not in self._cache:
                self._cache[instance] = self.compute_func(instance)
            return self._cache[instance]
    ```
    
- Lazy Loading Implementation
    
    ```python
    class LazyProperty:
        def __init__(self, function):
            self.function = function
            self._cache = {}
    
        def __get__(self, instance, owner): #follows the descriptor protocol
            # self - The descriptor object itself (the LazyProperty instance stored in the class).
            # instance - object whose attribute is being accessed.
            # owner - The class that owns the descriptor (the class where it was defined).
            # LazyProperty.__get__(descriptor_object, dp, DataProcessor)
            if instance is None:
                return self
            # Why instance ***is None*** is checked
            # If you access it from the class:
    	        # DataProcessor.complex_calculation
    	      # Python calls
    	      # __get__(descriptor, None, DataProcessor)
    
            if instance not in self._cache:
                self._cache[instance] = self.function(instance)
            return self._cache[instance]
    
    class DataProcessor:
        @LazyProperty
        def complex_calculation(self):
            ## Simulate expensive computation
            import time
            time.sleep(2)
            return sum(range(1000000))
    
    dp = DataProcessor()
    dp.complex_calculation 
    # Because **complex_calculation** is a **descriptor**, Python calls 
    # LazyProperty.__get__(self, instance, owner).
    ```
    
- Calling `property()` is a succinct way of building a data descriptor that triggers function calls upon access to an attribute.
    
    ```python
    property(fget=None, fset=None, fdel=None, doc=None) -> property attribute
    ```
    

**👍 Advantages 👍**

- Memory management.

**👎 Disadvantages 👎**

- Descriptors add a small **overhead** to attribute access
- Caching can mitigate performance impacts
- Use sparingly for complex operations

**↔️ Alternatives ↔️**

- Getter/Setter
- Properties

**✅ Best practices ✅**

- Keep descriptor logic simple and focused
- Use descriptors for cross-cutting concerns
- Consider performance implications
- Validate input thoroughly

**🛠️ Use cases 🛠️**

- Data validation
- Computed attributes
- Lazy loading of attributes
- Access control and permissions

**🛑 Worst practices 🛑**

- 

Sources:

[How to understand Python descriptor protocol | LabEx](https://labex.io/tutorials/python-how-to-understand-python-descriptor-protocol-450974)

# Properties

**🔽 What? 🔽**

- 

**🔁 What does it do? 🔁**

- 

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- 

🤔 **How does it work?** 🤔

- 

**✍️ How to use it? ✍️**

- `@property`

**👍 Advantages 👍**

- 

**👎 Disadvantages 👎**

- 

**↔️ Alternatives ↔️**

- 

**✅ Best practices ✅**

- The recommended and Pythonic approach

**🛠️ Use cases 🛠️**

- 

**🛑 Worst practices 🛑**

- 

Sources:

# Interface

**🔽 What? 🔽**

- 

**🔁 What does it do? 🔁**

- 

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- 

🤔 **How does it work?** 🤔

- 

**✍️ How to use it? ✍️**

- 

**👍 Advantages 👍**

- 

**👎 Disadvantages 👎**

- 

**↔️ Alternatives ↔️**

- 

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- 

**🛑 Worst practices 🛑**

- 

Sources:

[Python Interfaces: Why should a Data Scientist Care? | Towards Data Science](https://towardsdatascience.com/python-interfaces-why-should-a-data-scientist-care-2ed7ff80f225/)

[Using OOP interfaces in Python](https://www.reddit.com/r/Python/comments/1lvrkpg/using_oop_interfaces_in_python/)

# Software architecture patterns/styles

**🔽 What? 🔽**

- 

**🔁 What does it do? 🔁**

- 

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- 

🤔 **How does it work?** 🤔

- 

**✍️ How to use it? ✍️**

- 

**👍 Advantages 👍**

- 

**👎 Disadvantages 👎**

- 

**↔️ Alternatives ↔️**

- 

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- 

**🛑 Worst practices 🛑**

- 

Sources:

[List of software architecture styles and patterns](https://en.wikipedia.org/wiki/List_of_software_architecture_styles_and_patterns)

# Data Model

**🔽 What? 🔽**

- 

**🔁 What does it do? 🔁**

- 

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- 

🤔 **How does it work?** 🤔

- 

**✍️ How to use it? ✍️**

- 

**👍 Advantages 👍**

- it makes version control easier

**👎 Disadvantages 👎**

- 

**↔️ Alternatives ↔️**

- 

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- 

**🛑 Worst practices 🛑**

- 

Sources:

[3. Data model](https://docs.python.org/3/reference/datamodel.html)

# God Object

**🔽 What? 🔽**

- 

**🔁 What does it do? 🔁**

- 

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- 

🤔 **How does it work?** 🤔

- 

**✍️ How to use it? ✍️**

- 

**👍 Advantages 👍**

- 

**👎 Disadvantages 👎**

- 

**↔️ Alternatives ↔️**

- 

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- 

**🛑 Worst practices 🛑**

- 

Sources:

[God object](https://en.wikipedia.org/wiki/God_object)

# Multiple Class Constructors

**🔽 What? 🔽**

- 

**🔁 What does it do? 🔁**

- 

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- 

🤔 **How does it work?** 🤔

- 

**✍️ How to use it? ✍️**

- 

**👍 Advantages 👍**

- 

**👎 Disadvantages 👎**

- 

**↔️ Alternatives ↔️**

- 

**✅ Best practices ✅**

- PEP 443 therefore introduced **single-dispatch generic functions** to help you avoid using this coding anti-pattern whenever possible.
- A powerful technique for providing multiple constructors in Python is to use `@classmethod`. This decorator allows you to **turn a regular method into a class method**. Unlike regular methods, class methods **don’t take the current instance**, `self`, as an argument. Instead, they take the class itself, which is commonly passed in as the `cls` argument. Using `cls` to name this argument is a popular convention in the Python community.

**🛠️ Use cases 🛠️**

- 

**🛑 Worst practices 🛑**

- A pretty useful technique for **simulating multiple constructors** in a Python class is to provide `.__init__()` with **optional arguments** using **default argument values**. This way, you can call the class constructor in different ways and get a different behavior each time.
    
    ```python
    class CumulativePowerFactory:
        def __init__(self, exponent=2, *, start=0):
            self._exponent = exponent
            self.total = start
    
        def __call__(self, base):
            power = base ** self._exponent
            self.total += power
            return power
    ```
    
    ```python
    >>> from power import CumulativePowerFactory
    
    >>> square = CumulativePowerFactory()
    >>> square(21)
    441
    >>> square(42)
    1764
    >>> square.total
    2205
    
    >>> cube = CumulativePowerFactory(exponent=3)
    >>> cube(21)
    9261
    >>> cube(42)
    74088
    >>> cube.total
    83349
    
    >>> initialized_cube = CumulativePowerFactory(3, start=2205)
    >>> initialized_cube(21)
    9261
    >>> initialized_cube(42)
    74088
    >>> initialized_cube.total
    85554
    ```
    
- Another strategy is to check the **data type** of the arguments to `.__init__()` to provide different behaviors depending on the concrete data type that you pass in the call. This technique allows you to **simulate multiple constructors** in a class.
    
    ```python
    isinstance(42, int)
    isinstance(42, float)
    isinstance(42, (list, int))
    isinstance(42, list | int)  # Python >= 3.10
    ```
    
    ```python
    >>> from datetime import date
    
    >>> class Person:
    ...     def __init__(self, name, birth_date):
    ...         self.name = name
    ...         if isinstance(birth_date, date):
    ...             self.birth_date = birth_date
    ...         elif isinstance(birth_date, str):
    ...             self.birth_date = date.fromisoformat(birth_date)
    ...
    
    >>> jane = Person("Jane Doe", "2000-11-29")
    >>> jane.birth_date
    datetime.date(2000, 11, 29)
    
    >>> john = Person("John Doe", date(1998, 5, 15))
    >>> john.birth_date
    datetime.date(1998, 5, 15)
    ```
    

Sources:

[Providing Multiple Constructors in Your Python Classes – Real Python](https://realpython.com/python-multiple-constructors/)

# Meta Class

**🔽 What? 🔽**

- 

**🔁 What does it do? 🔁**

- defines how the classes will be created, not the object, and not the initioalization of class or object.

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- 

🤔 **How does it work?** 🤔

- 

**✍️ How to use it? ✍️**

- 

**👍 Advantages 👍**

- 

**👎 Disadvantages 👎**

- 

**↔️ Alternatives ↔️**

- 

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- Singleton classes creation

**🛑 Worst practices 🛑**

- 

Sources:

# GRASP

April 6, 2026 

**🔽 What? 🔽**

- General responsability assignment software patterns (or principles)

**🔁 What does it do? 🔁**

- 

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- to make software more **maintainable**,
    - **flexible**,
    - and **scalable**

🤔 **How does it work?** 🤔

- It is all about putting responsibilities in code structures such as classes/methods/modules in such a way it "makes sense".

**✍️ How to use it? ✍️**

- 

**👍 Advantages 👍**

- 

**👎 Disadvantages 👎**

- 

**↔️ Alternatives ↔️**

- 

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- 

**🛑 Worst practices 🛑**

- 

Sources:

[Unleashing the Power of GRASP Design Principles: A Guide to Building Robust Software with…](https://zikazaki.medium.com/unleashing-the-power-of-grasp-design-principles-a-guide-to-building-robust-software-with-7a2e23e055a8)

[Apply the GRASP Design Principles to Improve Your Python Code](https://www.youtube.com/watch?v=fGNF6wuD-fg)

## Creator

[Знати GRASP](https://www.notion.so/GRASP-331745f820dc8056980bd3c80b4d8be6?pvs=21) April 6, 2026 

**🔽 What? 🔽**

- principle

**🔁 What does it do? 🔁**

- suggests that a class should be **responsible** for **creating instances** of other classes or objects if it contains or aggregates them.

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- 

🤔 **How does it work?** 🤔

- By assigning this responsibility to the appropriate class, we establish a clear relationship between objects and their creators.

**✍️ How to use it? ✍️**

- Code example
    
    ```python
    class Customer:
        def place_order(self, items):
            order = Order(items)  # Creating an instance of Order
            # Further processing and interactions
    ```
    

**👍 Advantages 👍**

- 

**👎 Disadvantages 👎**

- 

**↔️ Alternatives ↔️**

- 

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- 

**🛑 Worst practices 🛑**

- 

Sources:

[Unleashing the Power of GRASP Design Principles: A Guide to Building Robust Software with…](https://zikazaki.medium.com/unleashing-the-power-of-grasp-design-principles-a-guide-to-building-robust-software-with-7a2e23e055a8)

[Apply the GRASP Design Principles to Improve Your Python Code](https://www.youtube.com/watch?v=fGNF6wuD-fg)

## Information Expert

[Знати GRASP](https://www.notion.so/GRASP-331745f820dc8056980bd3c80b4d8be6?pvs=21) April 6, 2026 

**🔽 What? 🔽**

- principle

**🔁 What does it do? 🔁**

- states that a responsibility should be assigned to the class or object that possesses the most information required to fulfill that responsibility.

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- to decide **where** (in which class, method, etc.) should developer assign **new responsabilities**
- By assigning responsibilities to classes with the necessary knowledge, we promote **encapsulation** and **maintainability**.

🤔 **How does it work?** 🤔

- You write the code in the closest part that has all the information
- 

**✍️ How to use it? ✍️**

- Example
    
    Imagine a scenario where we need to calculate the total price of an order. In this case, the “Order” class would be the information expert as it has **access** to **individual item prices and quantities**:
    
    ```python
    class Order:
        def __init__(self, items):
            self.items = items
        
        def calculate_total_price(self):
            total_price = 0
            for item in self.items:
                total_price += item.price * item.quantity
            return total_price
    
    ```
    

**👍 Advantages 👍**

- 

**👎 Disadvantages 👎**

- 

**↔️ Alternatives ↔️**

- 

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- 

**🛑 Worst practices 🛑**

- 

Sources:

[Unleashing the Power of GRASP Design Principles: A Guide to Building Robust Software with…](https://zikazaki.medium.com/unleashing-the-power-of-grasp-design-principles-a-guide-to-building-robust-software-with-7a2e23e055a8)

[Apply the GRASP Design Principles to Improve Your Python Code](https://www.youtube.com/watch?v=fGNF6wuD-fg)

## **Low Coupling**

[Знати GRASP](https://www.notion.so/GRASP-331745f820dc8056980bd3c80b4d8be6?pvs=21) April 6, 2026 

**🔽 What? 🔽**

- principle

**🔁 What does it do? 🔁**

- emphasizes **reducing dependencies** between classes or objects.

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- By minimizing the coupling, we achieve **flexibility**, **modularity**, and easier **maintenance**.

🤔 **How does it work?** 🤔

- 

**✍️ How to use it? ✍️**

- Example
    
    For instance, consider a scenario where a “PaymentProcessor” class interacts with a “PaymentGateway” class through an interface. This loose coupling allows for easy substitution of different payment gateways without impacting the rest of the system:
    
    ```python
    class PaymentProcessor:
        def process_payment(self, payment_gateway):
            payment_gateway.process_payment()
            # Further processing and error handling
    
    class PaymentGateway:
        def process_payment(self):
            # Payment processing logic
            pass
    ```
    

**👍 Advantages 👍**

- 

**👎 Disadvantages 👎**

- 

**↔️ Alternatives ↔️**

- Dependency Inversion Principle

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- 

**🛑 Worst practices 🛑**

- 

Sources:

[Unleashing the Power of GRASP Design Principles: A Guide to Building Robust Software with…](https://zikazaki.medium.com/unleashing-the-power-of-grasp-design-principles-a-guide-to-building-robust-software-with-7a2e23e055a8)

## **High Cohesion**

April 6, 2026 [Знати GRASP](https://www.notion.so/GRASP-331745f820dc8056980bd3c80b4d8be6?pvs=21) 

**🔽 What? 🔽**

- principle

**🔁 What does it do? 🔁**

- suggests that a class should have a clear and well-defined purpose, focusing on a single set of related responsibilities

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- By grouping related functions and data within a class, we achieve better organization and maintainability.

🤔 **How does it work?** 🤔

- 

**✍️ How to use it? ✍️**

- Example
    
    Let’s consider a “Car” class should have methods for starting the engine, accelerating, braking, and turning, rather than mixing unrelated functionalities:
    
    ```python
    class Car:
        def start_engine(self):
            # Start the engine logic
    
        def accelerate(self):
            # Acceleration logic
    
        def brake(self):
            # Braking logic
    
        def turn(self, direction):
            # Turning logic
    ```
    

**👍 Advantages 👍**

- 

**👎 Disadvantages 👎**

- 

**↔️ Alternatives ↔️**

- Single Responsibility

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- 

**🛑 Worst practices 🛑**

- 

Sources:

[Unleashing the Power of GRASP Design Principles: A Guide to Building Robust Software with…](https://zikazaki.medium.com/unleashing-the-power-of-grasp-design-principles-a-guide-to-building-robust-software-with-7a2e23e055a8)

## Controller

April 6, 2026 [Знати GRASP](https://www.notion.so/GRASP-331745f820dc8056980bd3c80b4d8be6?pvs=21) 

**🔽 What? 🔽**

- principle

**🔁 What does it do? 🔁**

- states that there should be a **class responsible** for **receiving and handling** system events or user **inputs**
- The controller class **manages the flow of information** and **coordinates the actions of other objects**.

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- 

🤔 **How does it work?** 🤔

- **Controller** is the first object that **receives** and handles any interaction with the system coming from the **User Interface**.

**✍️ How to use it? ✍️**

- Example
    
    For instance, in a web application, a “UserController” class could handle user registration, login, and profile update functionalities:
    
    ```python
    class UserController:
        def register_user(self, user_data):
            # User registration logic
        
        def login_user(self, credentials):
            # User login logic
        
        def update_profile(self, user_id, updated_data):
            # Profile update logic
    
    ```
    

**👍 Advantages 👍**

- 

**👎 Disadvantages 👎**

- 

**↔️ Alternatives ↔️**

- 

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- 

**🛑 Worst practices 🛑**

- 

Sources:

[Unleashing the Power of GRASP Design Principles: A Guide to Building Robust Software with…](https://zikazaki.medium.com/unleashing-the-power-of-grasp-design-principles-a-guide-to-building-robust-software-with-7a2e23e055a8)

[Unleashing the Power of GRASP Design Principles: A Guide to Building Robust Software with…](https://zikazaki.medium.com/unleashing-the-power-of-grasp-design-principles-a-guide-to-building-robust-software-with-7a2e23e055a8)

## **Pure Fabrication**

April 6, 2026 [Знати GRASP](https://www.notion.so/GRASP-331745f820dc8056980bd3c80b4d8be6?pvs=21) 

**🔽 What? 🔽**

- priniciple

**🔁 What does it do? 🔁**

- suggests creating **classes** that do **not** represent **real-world concepts** but are designed **to handle complex operations** or fulfill specific system needs.

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- These classes act as **helpers** or intermediaries, contributing to a more **modular** and **maintainable** design

🤔 **How does it work?** 🤔

- 

**✍️ How to use it? ✍️**

- Example
    
    For instance, a “FileParser” class responsible for parsing specific file formats can be considered a pure fabrication:
    
    ```python
    class FileParser:
        def parse_csv(self, file_path):
            # CSV parsing logic
    
        def parse_json(self, file_path):
            # JSON parsing logic
    
        def parse_xml(self, file_path):
            # XML parsing logic
    ```
    

**👍 Advantages 👍**

- 

**👎 Disadvantages 👎**

- 

**↔️ Alternatives ↔️**

- 

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- 

**🛑 Worst practices 🛑**

- 

Sources:

[Unleashing the Power of GRASP Design Principles: A Guide to Building Robust Software with…](https://zikazaki.medium.com/unleashing-the-power-of-grasp-design-principles-a-guide-to-building-robust-software-with-7a2e23e055a8)

## **Indirection**

April 6, 2026 [Знати GRASP](https://www.notion.so/GRASP-331745f820dc8056980bd3c80b4d8be6?pvs=21) 

**🔽 What? 🔽**

- principle

**🔁 What does it do? 🔁**

- advises introducing an intermediate class or object **to decouple two classes** that have a **direct relationship**.

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- Indirection **reduces dependencies** and provides flexibility to change or extend the system.

🤔 **How does it work?** 🤔

- 

**✍️ How to use it? ✍️**

- Example
    
    For example, a “Logger” class can act as an intermediary **between multiple classes**, allowing them to log messages without directly coupling to a specific logging implementation:
    
    ```python
    class Logger:
        def log_message(self, message):
            # Logging logic
            pass
    
    class SomeClass:
        def __init__(self, logger):
            self.logger = logger
    
        def do_something(self):
            self.logger.log_message("Doing something")
    ```
    

**👍 Advantages 👍**

- 

**👎 Disadvantages 👎**

- 

**↔️ Alternatives ↔️**

- 

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- 

**🛑 Worst practices 🛑**

- 

Sources:

[Unleashing the Power of GRASP Design Principles: A Guide to Building Robust Software with…](https://zikazaki.medium.com/unleashing-the-power-of-grasp-design-principles-a-guide-to-building-robust-software-with-7a2e23e055a8)

## **Protected Variations**

April 6, 2026 [Знати GRASP](https://www.notion.so/GRASP-331745f820dc8056980bd3c80b4d8be6?pvs=21) 

**🔽 What? 🔽**

- principle

**🔁 What does it do? 🔁**

- emphasizes **identifying** and **encapsulating** the parts of a system that are likely to change due to external factors.

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- By **isolating and protecting** these variations, we minimize the **impact of changes** and create a more **robust and adaptable design**.

🤔 **How does it work?** 🤔

- 

**✍️ How to use it? ✍️**

- Example
    
    Consider a scenario where we have a “DataStore” class that provides access to a database. To protect against changes in the database technology or schema, we can encapsulate the database-specific logic within the “DataStore” class:
    
    ```python
    class DataStore:
        def __init__(self, db_connection):
            self.db_connection = db_connection
    
        def fetch_data(self):
            # Database query and data retrieval logic
    
        def save_data(self, data):
            # Database insert/update logic
    ```
    

**👍 Advantages 👍**

- 

**👎 Disadvantages 👎**

- 

**↔️ Alternatives ↔️**

- 

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- 

**🛑 Worst practices 🛑**

- 

Sources:

[Unleashing the Power of GRASP Design Principles: A Guide to Building Robust Software with…](https://zikazaki.medium.com/unleashing-the-power-of-grasp-design-principles-a-guide-to-building-robust-software-with-7a2e23e055a8)

# **KISS**

April 6, 2026 

**🔽 What? 🔽**

- *“Keep it simple, stupid!”*
- Clean code principle

**🔁 What does it do? 🔁**

- This principle champions simplicity in code design

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- **Maintainer's Dream**: Simple **code** is inherently more **adaptable**, allowing for **easier modifications and updates**.
- **Clear Communication**: Code that is easy to read and understand facilitates **collaboration** and comprehension **among developers**.
- **Testing Made Easy**: Simpler logic reduces the complexity of automated testing, thus enhancing reliability across unit and integration tests.
- **Scalability**: Simple systems scale more efficiently. When you’re not bogged down by excessive complexity, it’s easier to build on top of your existing codebase. Simple foundations allow for flexible extensions and enhancements.

🤔 **How does it work?** 🤔

- It encourages developers to **avoid unnecessary complexity** and instead write code that is **straightforward** and **clear**. While simple, the term "KISS" encompasses a variety of **refactoring techniques** aimed at maintaining **simplicity** throughout the coding process.
- Common pitfalls when violating KISS (purposes to use KISS):
    - **Overengineering:** Developers might be tempted to **plan for every possible future scenario**, introducing features that **aren’t necessary today**. This leads to code bloat, making the system **unnecessarily complex**.
    - **Cleverness over Clarity:** Writing clever code might **feel rewarding**, but the problem arises when future developers (or even the original developer after some time) **struggle to understand** the logic behind it.
    - **Premature Optimization:** While optimizing code for performance is essential, doing it too early, before you fully understand the problem, can lead to **convoluted and complex solutions**. Simple, clear code is often sufficient for most applications, and only critical performance bottlenecks should be optimized **after profiling**.

**✍️ How to use it? ✍️**

- Key strategies for implementing the **KISS principle**:
    - **Write Smaller Programs**: Keep your methods and classes concise. Aim to solve one problem at a time.
    - **Remove Unused Code**: Eliminate superfluous methods and instances that **serve no purpose**, reducing clutter and potential confusion.
    - Favor **readability over cleverness**: Write code as **if you’re explaining it** to someone with **less experience**. If someone can easily understand what the code does, you’ve likely kept it simple. Write code that is transparent and straightforward for others to follow.
    - **Employ Composition**: Use existing code effectively by **composing simple pieces** instead of rewriting functionality.
    - **Modular Programming**: Break down your application into modules that can function independently. This approach aids in organization and enhances flexibility.
    - **Avoid unnecessary abstractions:** Do**n’t** introduce **design patterns or abstractions** unless they are genuinely needed.
    - **Iterate:** Refactor often. As you gain more insight into the problem you’re solving, **simplify** your code **wherever possible**.

**👍 Advantages 👍**

- 

**👎 Disadvantages 👎**

- 

**↔️ Alternatives ↔️**

- SOLID
- YAGNI

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- 

**🛑 Worst practices 🛑**

- 

Sources:

[Understanding the “KISS” Principle in Software Design: Keep It Simple, Stupid](https://medium.com/@Masoncoding/understanding-the-kiss-principle-in-software-design-keep-it-simple-stupid-6f5fcd8913f3)

[Applying the KISS Principle in Python](https://codesignal.com/learn/courses/applying-clean-code-principles-in-python/lessons/applying-the-kiss-principle-in-python)

# DRY

April 6, 2026 

**🔽 What? 🔽**

- **Don't Repeat Yourself**

**🔁 What does it do? 🔁**

- 

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- to eliminate redundancy in code.
- for writing efficient, maintainable, and clean code.
- **Reduction of Complexity.** First and foremost, it reduces code complexity by avoiding unnecessary repetitions. This makes the code more readable, clear, and easier to understand for developers.

🤔 **How does it work?** 🤔

- Issues that affect the efficiency and maintainability of software:
    - **Code Bloat**: Repeating similar code across different parts of your application **unnecessarily increases the size of the codebase**. This makes the code **harder** to **navigate** and increases the chances of **introducing errors**.
    - **Risk of Inconsistencies**: When similar pieces of logic are scattered across different areas, they can easily become **out of sync** during updates or bug fixes. This can result in logic discrepancies and potentially introduce new problems.
    - **Maintenance Challenges**: Updating code often requires modifications in multiple places, leading to increased work and a **higher likelihood of errors**. Redundant code makes it difficult for developers to ensure all necessary changes have been made consistently.

**✍️ How to use it? ✍️**

- DRY Strategies:
    - **Extracting Function**: Move repeated logic into a **dedicated function** that can be reused wherever needed. This promotes reuse and simplifies updates.
    - **Extracting Variable**: Consolidate **repeated expressions or values** into **variables**. This centralizes change, reducing the potential for errors.
    - **Replace Temp with Function**: Use a function to compute values on demand rather than storing them in **temporary variables**, aiding in readability and reducing redundancy.

**👍 Advantages 👍**

- 

**👎 Disadvantages 👎**

- 

**↔️ Alternatives ↔️**

- 

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- 

**🛑 Worst practices 🛑**

- 

Sources:

[Applying the DRY Principle in Python](https://codesignal.com/learn/courses/applying-clean-code-principles-in-python/lessons/applying-the-dry-principle-in-python)

[Principles of Software Development: SOLID, DRY, KISS, and more](https://scalastic.io/en/solid-dry-kiss/#dry-dont-repeat-yourself)

# **YAGNI**

April 6, 2026 

**🔽 What? 🔽**

- **You Ain’t Gonna Need It**
- principle

**🔁 What does it do? 🔁**

- emphasizes not implementing features or code that are not immediately necessary.

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- to **avoid over-engineering**,
    - **reduce complexity**,
    - and **focus** on the immediate **needs of users**

🤔 **How does it work?** 🤔

- According to this principle, it’s better to focus on essential features and **avoid** anticipating **hypothetical future needs**.

**✍️ How to use it? ✍️**

- To apply the YAGNI principle, it’s important to ask the question, “*Do I really need it now?*” before adding a new feature or developing additional code. Carefully **evaluate** the **importance and urgency** of the functionality and **avoid preemptive additions** based on uncertain assumptions. **Prioritize essential features** and focus on the **real needs of users**.

**👍 Advantages 👍**

- It **reduces** code **complexity** by avoiding the addition of unnecessary features.
- his makes the **code clearer**, lighter, and **easier to maintain**.
- It **saves time and resources** by avoiding the development and testing of features that might **never be used**.
- It promotes an **iterative approach** to development by **focusing** on the **immediate needs** of **users** and allowing the addition of additional features as they become **genuinely necessary**.

**👎 Disadvantages 👎**

- 

**↔️ Alternatives ↔️**

- 

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- 

**🛑 Worst practices 🛑**

- 

Sources:

[Principles of Software Development: SOLID, DRY, KISS, and more](https://scalastic.io/en/solid-dry-kiss/#yagni-you-aint-gonna-need-it)