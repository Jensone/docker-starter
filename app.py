from flask import Flask, render_template_string
import random
import os

app = Flask(__name__)

@app.route('/')
def cv():
    # Compétences DevOps aléatoires
    devops_skills = [
        "Docker", "Kubernetes", "Jenkins", "GitLab CI/CD", "GitHub Actions", 
        "Terraform", "Ansible", "Puppet", "AWS", "Azure", "GCP", 
        "Prometheus", "Grafana", "ELK Stack", "Datadog", "Nagios",
        "Linux", "Shell Scripting", "Python", "Go", "Bash"
    ]
    
    # Expériences aléatoires
    experiences = [
        {
            "titre": "Ingénieur DevOps Senior",
            "entreprise": "TechCloud Solutions",
            "periode": "2022 - Présent",
            "description": "Mise en place et maintenance de l'infrastructure cloud, automatisation des déploiements et optimisation des performances."
        },
        {
            "titre": "Administrateur Systèmes",
            "entreprise": "DataSync Technologies",
            "periode": "2020 - 2022",
            "description": "Gestion des serveurs Linux, mise en place de solutions de monitoring et de sécurité."
        },
        {
            "titre": "Développeur Backend",
            "entreprise": "WebScale Inc.",
            "periode": "2018 - 2020",
            "description": "Développement d'API RESTful et implémentation de CI/CD pour les applications web."
        }
    ]
    
    # Projets aléatoires
    projets = [
        {
            "nom": "Migration vers Kubernetes",
            "description": "Migration d'une architecture monolithique vers des microservices sur Kubernetes."
        },
        {
            "nom": "Automatisation du déploiement",
            "description": "Mise en place d'un pipeline CI/CD pour automatiser les tests et les déploiements."
        },
        {
            "nom": "Monitoring et alerting",
            "description": "Implémentation d'un système de monitoring avec Prometheus et Grafana."
        }
    ]
    
    # Certifications aléatoires
    certifications = [
        "AWS Certified DevOps Engineer - Professional",
        "Certified Kubernetes Administrator (CKA)",
        "Microsoft Certified: Azure DevOps Engineer Expert",
        "Docker Certified Associate",
        "Terraform Associate",
        "GitLab Certified",
        "Google Professional Cloud DevOps Engineer"
    ]
    
    # Sélection aléatoire des compétences, expériences, projets et certifications
    selected_skills = random.sample(devops_skills, 10)
    selected_experiences = random.sample(experiences, min(len(experiences), 2))
    selected_projets = random.sample(projets, min(len(projets), 2))
    selected_certifications = random.sample(certifications, 3)
    
    # Template HTML pour afficher le CV
    template = """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CV DevOps</title>
        <style>
            body {
                font-family: 'Arial', sans-serif;
                line-height: 1.6;
                margin: 0;
                padding: 20px;
                background-color: #f5f5f5;
                color: #333;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                background-color: #fff;
                padding: 30px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
                border-radius: 5px;
            }
            header {
                text-align: center;
                margin-bottom: 30px;
                border-bottom: 2px solid #2c3e50;
                padding-bottom: 20px;
            }
            h1 {
                color: #2c3e50;
                margin-bottom: 10px;
            }
            h2 {
                color: #3498db;
                border-bottom: 1px solid #eee;
                padding-bottom: 10px;
                margin-top: 30px;
            }
            .skills {
                display: flex;
                flex-wrap: wrap;
                gap: 10px;
                margin-top: 15px;
            }
            .skill {
                background-color: #3498db;
                color: white;
                padding: 5px 10px;
                border-radius: 3px;
                font-size: 14px;
            }
            .experience, .project, .certification {
                margin-bottom: 20px;
            }
            .experience h3, .project h3 {
                color: #2c3e50;
                margin-bottom: 5px;
            }
            .periode {
                font-style: italic;
                color: #7f8c8d;
            }
            .contact {
                margin-top: 10px;
                color: #7f8c8d;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>{{ nom }}</h1>
                <p>{{ titre }}</p>
                <div class="contact">
                    <p>{{ email }} | {{ telephone }}</p>
                    <p>{{ adresse }}</p>
                </div>
            </header>
            
            <section>
                <h2>Compétences</h2>
                <div class="skills">
                    {% for skill in skills %}
                    <span class="skill">{{ skill }}</span>
                    {% endfor %}
                </div>
            </section>
            
            <section>
                <h2>Expériences Professionnelles</h2>
                {% for exp in experiences %}
                <div class="experience">
                    <h3>{{ exp.titre }} - {{ exp.entreprise }}</h3>
                    <p class="periode">{{ exp.periode }}</p>
                    <p>{{ exp.description }}</p>
                </div>
                {% endfor %}
            </section>
            
            <section>
                <h2>Projets</h2>
                {% for projet in projets %}
                <div class="project">
                    <h3>{{ projet.nom }}</h3>
                    <p>{{ projet.description }}</p>
                </div>
                {% endfor %}
            </section>
            
            <section>
                <h2>Certifications</h2>
                {% for cert in certifications %}
                <div class="certification">
                    <p>{{ cert }}</p>
                </div>
                {% endfor %}
            </section>
        </div>
    </body>
    </html>
    """
    
    # Données aléatoires pour le profil
    data = {
        "nom": "Alex Dupont",
        "titre": "Ingénieur DevOps Senior",
        "email": "alex.dupont@example.com",
        "telephone": "+33 6 12 34 56 78",
        "adresse": "Paris, France",
        "skills": selected_skills,
        "experiences": selected_experiences,
        "projets": selected_projets,
        "certifications": selected_certifications
    }
    
    return render_template_string(template, **data)

if __name__ == '__main__':
    # Config pour que l'app tourne dans le conteneur
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
