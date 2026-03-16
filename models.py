# models.py
# This file defines the data structure (blueprint) for our objects
# Using OOP (Object-Oriented Programming) - good for viva!


class Project:
    """Represents a freelance project."""

    def __init__(self, project_name, client_name, freelancer, deadline,
                 status="Pending", payment_status="Unpaid", project_id=None):
        self.id = project_id
        self.project_name = project_name
        self.client_name = client_name
        self.freelancer = freelancer
        self.deadline = deadline
        self.status = status                  # Pending / Completed
        self.payment_status = payment_status  # Paid / Unpaid

    def __repr__(self):
        return f"Project({self.project_name}, {self.client_name}, {self.status})"


class Freelancer:
    """Represents a freelancer."""

    def __init__(self, name, skill, email, freelancer_id=None):
        self.id = freelancer_id
        self.name = name
        self.skill = skill
        self.email = email

    def __repr__(self):
        return f"Freelancer({self.name}, {self.skill})"