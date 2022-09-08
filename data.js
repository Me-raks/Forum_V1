module.exports = () => {
  const firstUser = {
    id: 1,
    username: "salydgn",
    password: "password",
    avatar: "../static/img/avatar.png",
    bio: "Je suis salydgn",
  };
  const firstDiscussion = {
    id: 1,
    titre: "Ma première discussion",
    auteurId: 1,
    tagsId: [1, 2, 3],
    timestamp: "22/06/2022 à 17h10",
    contenu: "Je suis la première discussion du forum Simulamath",
    nombreDePosts: 10,
    description: "Première",
    sousCategorie: 15,
  };
  const firstPost = {
    id: 1,
    discussionId: 1,
    contenu: "Première réponse à la première discussion du forum",
    nombreDeLikes: 10,
    nombreDeDislikes: 0,
    timestamp: "22/06/2022 à 17h11",
    auteurId: 2,
  };
  var casual = require("casual");

  const sousCategories = [
    {
      id: 1,
      nom: "Analyse-&-algèbre",
      categorie: "Enseignement-Moyen",
    },
    {
      id: 2,
      nom: "Graphique-2D-et-3D",
      categorie: "Enseignement-Moyen",
    },
    {
      id: 3,
      nom: "Probalité",
      categorie: "Enseignement-Moyen",
    },
    {
      id: 4,
      nom: "Statistique",
      categorie: "Enseignement-Moyen",
    },
    {
      id: 5,
      nom: "Analyse-&-algèbre",
      categorie: "Enseignement-Secondaire",
    },
    {
      id: 6,
      nom: "Graphique-2D-et-3D",
      categorie: "Enseignement-Secondaire",
    },
    {
      id: 7,
      nom: "Probalité",
      categorie: "Enseignement-Secondaire",
    },
    {
      id: 8,
      nom: "Statistique",
      categorie: "Enseignement-Secondaire",
    },
    {
      id: 9,
      nom: "Programmation",
      categorie: "Enseignement-Secondaire",
    },
    {
      id: 10,
      nom: "Analyse-&-algèbre",
      categorie: "Enseignement-Superieur",
    },
    {
      id: 11,
      nom: "Graphique-2D-et-3D",
      categorie: "Enseignement-Superieur",
    },
    {
      id: 12,
      nom: "Probalité",
      categorie: "Enseignement-Superieur",
    },
    {
      id: 13,
      nom: "Statistique",
      categorie: "Enseignement-Superieur",
    },
    {
      id: 14,
      nom: "Programmation",
      categorie: "Enseignement-Superieur",
    },
    {
      id: 15,
      nom: "Actualités",
      categorie: "Communauté",
    },
    {
      id: 16,
      nom: "Bugs-et-Suggestions",
      categorie: "Communauté",
    },
    {
      id: 17,
      nom: "Aide-aux-nouveaux",
      categorie: "Communauté",
    },
  ];

  const data = {
    user: [firstUser],
    discussion: [firstDiscussion],
    post: [firstPost],
    tag: [],
    sousCategorie: sousCategories,
  };
  // Create users
  for (let i = 2; i < 15; i++) {
    data.user.push({
      id: i,
      username: casual.username,
      password: "password",
      avatar: "../static/img/avatar.png",
      bio: casual.sentence,
    });
  }

  for (let i = 2; i < 20; i++) {
    data.discussion.push({
      id: i,
      title: casual.title,
      auteurId: casual.integer((from = 1), (to = 14)),
      tagsId: casual.array_of_digits((n = 2)),
      timestamp: `${casual.date((format = "DD-MM-YYYY"))} à ${casual.time(
        (format = "HH:mm:ss")
      )}`,
      contenu: casual.sentences((n = 4)),
      nombreDePosts: casual.integer((from = 1), (to = 25)),
      description: casual.short_description,
      sousCategorie: casual.integer((from = 1), (to = 17)),
    });
  }

  for (let i = 2; i < 250; i++) {
    data.post.push({
      id: i,
      discussionId: casual.integer((from = 1), (to = 19)),
      contenu: casual.sentences((n = 5)),
      nombreDeLikes: casual.integer((from = 0), (to = 14)),
      nombreDeDislikes: casual.integer((from = 0), (to = 14)),
      auteurId: casual.integer((from = 1), (to = 14)),
      timestamp: `${casual.date((format = "DD-MM-YYYY"))} à ${casual.time(
        (format = "HH:mm:ss")
      )}`,
    });
  }

  for (let i = 1; i < 25; i++) {
    data.tag.push({
      id: i,
      nom: `tag${i}`,
    });
  }
  return data;
};
