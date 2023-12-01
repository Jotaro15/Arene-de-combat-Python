import random

"""
    #Etape 1
    Créer une classe Hero.
    Un Héro doit avoir un nom, et une méthode publique nommée talk()
    Créez deux Héros, ces derniers doivent s'appeler Jay et Silent Bob.
    Faites en sorte que nos deux protagonistes parlent et aient une réplique différente.
    
    #Etape 2
    Nos deux protagonistes sont en désaccord.
    Faites en sorte qu'ils aient des points de vie et qu'un tape l'autre, lui ôtant des PV.
    
    #Etape 3
    Les PV sont-ils privés ou publics?
    Quelles méthodes sont à mettre en place?
    
    #Etape 4
    Commencez à concevoir votre histoire et décliner les types de héros. 
    Vous pourriez par exemple simuler un combat : 
    - Classe Héro : Barbare
        - Un barbare ayant des points de rage.
        - Il peut utiliser sa rage pour réaliser une attaque spéciale. Infligeant un dégat supérieur aléatoire.
        - A chaque tour il gagne un peu de rage jusque sa limite de rage.
    - Classe Magicien
        - Consomme de la mana
        - Peut lancer un sort de poison
        - Le magicien regagne de la mana avec le temps jusque sa limite de mana
    - Classe Soldat
        - Attaque classique
        - Equipement : Epée, Armure
    
    #Etape 5
    Ajoutez une arène, au sein de cette dernière, nous allons lancer un combat entre Héros.
    Ces derniers s'affrontent en tour par tour
    La partie continue tant qu'il reste plus d'un Héro en vie
    Un Héro Barbare gagne de la rage à la fin de chaque tour
    Un Héro Mage gagne du mana à la fin de chaque tour
    
    #Etapes suivantes en attendant
    Ajouter des :
        - Enemis communs par ex: Orc, Gobelin,  Troll des montagnes. 
                → Si un enemi commun entre dans l'arène, leurs combats s'arrêtent pour taper ensemble sur cet enemi.
        - Armes : Epée, Epée à deux mains, Baton 
        - Armure, bouclier, cape
        - Equipements supplémentaires : potions (soins, invincibilité)
            → Les héros commencent automatiquement avec un équipement supplémentaire aléatoire
    Définissez leurs règles et fonctionnement.  Déclinez le thème selon vos envies.

    #Bonus
    Ajoutez une classe voleur. 
    Ce dernier peut voler un item appartenant a un joueur. 
    Les items étant les armes, armures ou des équipements. 

    Le mage peut lancer un sort de feu désactivant les items métaliques adversaires.

    Les items ont une jauge d'usure, a chaque utilisation ils se consomment.
    Ex : Une potion de vie peut être utilisée deux fois. Une épée s'use à chaque attaque et se détruit au 10e coup etc...
"""

class Hero:
    """
    Les héros sont des combattants de l'arène qui ont une attaque de base et une attaque spéciale.
    Il peuvent aussi avoir des items et des potions.
    Ils combattent en priorité les méchants et se combattent entre eux dès qu'il n'y a plus de méchants.
    """
    def __init__(self, name, hero_type, pv):
        """
        On associe les noms,  attaques, types (Magicien, Soldat ou Barbare) et pv aux attributs associés.
        """
        self.name = name
        self.hero_type = hero_type
        self.pv = pv
        self.attacks = {"Magicien": {"base": 3, "poison": 5},  # On donne les dmg des attaques de base et spéciales pour chaque type
                        "Soldat": {"base": 3, "equipement": 2},
                        "Barbare": {"base": 5, "rage": 6}}
        self.special_attacks_counter = 0 #Les attaques spéciales se lancent à partir d'un certain nb de tour, donc on a un compteur de lancé
        self.luck_counter = 0

    def attack(self, target):
        """
        On définit l'attaque de tous les héros, un par un.
        On définit aussi la notion de priorité (les héros attaquent d'abord les méchants, puis s'attaquent entre eux.
        """
        if isinstance(target, Mechant): #quand la cible est un méchant
            target.pv -= self.attacks[self.hero_type]["base"]
            print(f"⚔{self.name} attaque {target.name} pour {self.attacks[self.hero_type]['base']} points de dégâts. Il lui reste {target.pv}pv.")

        else:
            for mechant in self.mechants: #quand un méchant attaque un méchant
                if mechant.pv > 0: #tant qu'il est en vie (qu'il a + de 0 pv)
                    mechant.pv -= self.attacks[self.hero_type]["base"] 
                    print(f"⚔{self.name} attaque {mechant.name} pour {self.attacks[self.hero_type]['base']} points de dégâts. Il lui reste {target.pv}pv.")

            for hero in self.heroes: #quand un héro attaque un héro
                if hero != self and hero.pv > 0: #tant qu'il est en vie (qu'il a + de 0 pv)
                    hero.pv -= self.attacks[self.hero_type]["base"]
                    print(f"⚔{self.name} attaque {hero.name} pour {self.attacks[self.hero_type]['base']} points de dégâts. Il lui reste {target.pv}pv.")

        self.special_attacks_counter += 1 #les 2 compteur pour les attaques spéciales et la chance augmentent de +1 à chaque tour
        self.luck_counter += 1
        if self.hero_type == "Magicien" and self.special_attacks_counter % 3 == 0:#attaque spéciale du Magicien (attaque poison) se déclenche au bout de 3 tours
            target.pv -= self.attacks[self.hero_type]["poison"] #attaque du type de héro est automatiquement son attaque spéciale
            print(f"☠{self.name} lance une attaque poison sur {target.name} pour {self.attacks[self.hero_type]['poison']} points de dégâts. Il lui reste {target.pv}pv.")

        #if self.hero_type == "Magicien" and self.luck_counter % 5 == 0 # Quand la chance du Magicien a augmenté de 5, il trouve "par hasard" une potion de soin.
            #self.pv[self.hero_type] += 
        if isinstance(target, Mechant) and target.pv <= 0 and self.hero_type == "Soldat": #attaque spéciale du Soldat (les équipements)
            self.attacks[self.hero_type]["base"] += self.attacks[self.hero_type]["equipement"] #les dégats de l'équipement s'ajoutent aux dégats de l'attaque de base
            print(f"🗡{self.name} gagne un équipement et son attaque augmente de {self.attacks[self.hero_type]['equipement']} points")
            
        if self.hero_type == "Barbare" and self.special_attacks_counter % 3 == 0: #attaque spéciale du Barbare (rage)
            target.pv -= self.attacks[self.hero_type]["rage"] #attaque du type de héro est automatiquement son attaque spéciale
            print(f"🔥{self.name} lance une attaque rage sur {target.name} pour {self.attacks[self.hero_type]['rage']} points de dégâts. Il lui reste {target.pv}pv.")

        if isinstance(target, Hero) and target.pv <= 0:
            print(f"🕱{target.name} est mort !") #quand les pv atteignent 0, on affiche que le héro est mort.
            
    def potion(self):
        """
        Quand un héro fait appel à la méthode potion (il boit une potion de healh), il reçoit un nb de pv aléatoire entre 5 et 15pv.
        """
        pv_bonus = random.randint(5, 15) #la potion donne entre 5 et 15pv
        self.pv += pv_bonus #les pv des héros sont augmentés du nb de pv de la potion
        print(f"✧{self.name} a reçu une potion et a gagné {pv_bonus} points de vie ! Il a désormais {self.pv}pv !")

class Magicien(Hero):
    """
    La classe Magicien appartient à la classe Héro.
    """
    def __init__(self, name, pv): #on associe la classe Magicien avec ses valeurs nom et pv
        super().__init__(name, "Magicien", pv)

class Soldat(Hero):
    """
    La classe Soldat appartient à la classe Héro.
    """
    def __init__(self, name, pv): #on associe la classe Soldat avec ses valeurs nom et pv
        super().__init__(name, "Soldat", pv)

class Barbare(Hero):
    """
    La classe Barbare appartient à la classe Héro.
    """
    def __init__(self, name, pv): #on associe la classe Barbare avec ses valeurs nom et pv
        super().__init__(name, "Barbare", pv)

class Mechant:
    """
    Les méchants vont combattre dans l'arène contre les héros.
    Ils ne s'attaquent pas entre méchants.
    """
    def __init__(self, name, mechant_type, pv):
        """
        On associe les noms,  attaques, types (Gobelin ou Ogre) et pv aux attributs associés.
        """
        self.name = name
        self.mechant_type = mechant_type
        self.pv = pv
        self.attacks = {"Gobelin": {"base": 2}, # On donne les dmg des attaques de base pour chaque type
                        "Ogre": {"base": 4}}

    def attack(self, targets):
        """
        On définit l'attaque des méchants.
        Tant qu'il y a  des héros vivants, les méchants leur tape dessus.
        Les méchants choisissent leur cible au hasard parmi les héros.
        """
        alive_heroes = [target for target in targets if isinstance(target, Hero) and target.pv > 0]
        if not alive_heroes:
            return

        target = random.choice(alive_heroes)
        target.pv -= self.attacks[self.mechant_type]["base"]
        print(f"⚔ {self.name} attaque {target.name} pour {self.attacks[self.mechant_type]['base']} points de dégâts. Il lui reste {target.pv}pv.")
        
class Arene:
    """
    C'est dans l'Arene que les héros et les méchants vont se battre. Il ne peut y avoir qu'un seul vainqueur, et c'est le dernier en vie.
    C'est aussi dans l'Arene que l'utiisateur peut choisir le nombre de méchants, et tous les héros qui se battrons.
    """
    def __init__(self):
        """
        La fonction __init__ contient le 'formulaire' que l'utlisateur remplit avant de commencer la partie pour créer les héros et les méchants.
        """
        self.is_finished = False
        self.heroes = []
        self.mechants = []
        
        num_gobelins = int(input("Combien de gobelins voulez-vous dans l'arène ? "))
        num_ogres = int(input("Combien d'ogres voulez-vous dans l'arène ? "))
        
        for i in range(num_gobelins):
            name = input(f"Nom du gobelin {i+1} : ")
            self.mechants.append(Mechant(name, "Gobelin", 10)) #on initialise le nom rentré par l'utilisateur avec son type et ses pv
            
        for i in range(num_ogres):
            name = input(f"Nom de l'ogre {i+1} : ")
            self.mechants.append(Mechant(name, "Ogre", 15)) #on initialise le nom rentré par l'utilisateur avec son type et ses pv
            
        for i in range(3):
            name = input(f"Nom du héros {i+1} : ")
            hero_type = input(f"Type du héros {i+1} (Magicien, Soldat ou Barbare) : ")
            pv = int(input(f"PV du héros {i+1} : "))
            
            if hero_type == "Magicien":
                self.heroes.append(Magicien(name, pv)) #on initialise le nom rentré par l'utilisateur avec son type et ses pv
            elif hero_type == "Soldat":
                self.heroes.append(Soldat(name, pv)) #on initialise le nom rentré par l'utilisateur avec son type et ses pv
            elif hero_type == "Barbare":
                self.heroes.append(Barbare(name, pv)) #on initialise le nom rentré par l'utilisateur avec son type et ses pv
        
    def start(self):
        """
        On lance la partie grâce à l'appel de cette fonction. Une fois la partie lancée, celle-ci va tourner jusqu'à ce qu'il n'y ait plus qu'1 survivant.
        """
        print("☞Début de la partie. Bon courage !")
        while not self.is_finished:
            alive_heroes = [hero for hero in self.heroes if hero.pv > 0] #nb de héro qui ont + de 0 pv
            alive_mechants = [mechant for mechant in self.mechants if mechant.pv > 0] #nb de méchants qui ont + de 0pv
            if not alive_heroes or not alive_mechants:
            #quand il n'y plus aucun combattant vivant, le jeu s'arrête
                self.is_finished = True
                continue
            
            for hero in self.heroes:
                if hero.pv <= 0:
                    continue #tant que le héro est vivant, il continue d'attaquer à chaque tour
                targets = alive_mechants.copy() #pour les héros, la priorité c'est les méchants. 
                if not len(targets): # Il n'y a plus de méchants à taper
                    targets.extend([h for h in alive_heroes if h != hero])
                if targets:
                    target = random.choice(targets) #avec random, on choisi le héro choisi aléatoirement une cible
                    hero.attack(target) #il attaque toujours sa cible
            for mechant in self.mechants:
                if mechant.pv <= 0: #tant que le méchant est vivant, il continue d'attaquer à chaque tour
                    continue
                targets = alive_heroes.copy() #pour les méchants, la priorité c'est les héros
                if targets:
                    mechant.attack(targets) #il attaque toujours sa cible

if __name__ == '__main__':
    Arene().start() #la partie se lance automatiquement à chaque fois qu'on "run" grace à l'appel de la méthode 'start'
