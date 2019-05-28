var drawbutton = document.getElementById('draw');
var c = document.getElementById("c");

var myturn = false;
var turn = document.getElementById('turn');

var deck = [];
var nursery = [];
var player_hand = [];
var opponent_hand = [];

var make_card = function(name, att){
    var card = document.createElementNS("http://www.w3.org/2000/svg", "image");
    card.setAttributeNS("http://www.w3.org/1999/xlink","xlink:href", "https://raw.githubusercontent.com/tfabiha/unstablepics/master/back.jpg");
    card.setAttribute("width",200);
    card.setAttribute("height",200);
    card.setAttribute("x", 0);
    card.setAttribute("y", 200);
    card.setAttribute("name", name);
    card.setAttribute("att", att);
    return card
};

d3.json("https://raw.githubusercontent.com/tfabiha/cerealmafia/master/static/cards.json", function(error, d) {
  var i;
  for (i = 0; i < d.length; i++) {
    var j;
    for (j = 0; j < d[i]["quantity"]; j++) {
      var x = make_card(d[i]["card_name"], d[i]["description"]);
      if (d[i]["card_type"] == "baby_uni") {
        x.setAttribute("x", 200);
        nursery.push(x);
      }else{
        deck.push(x);
      }
    }
  }
  var shuffle = function(deck) {
    var i, j, k;
    for(i = deck.length - 1; i > 0; i--) {
      j = Math.floor(Math.random() * (i+1));
      temp = deck[i];
      deck[i] = deck[j];
      deck[j] = temp;
    }
  };

  shuffle(nursery);
  shuffle(deck);

  var make_player_hand = function() {
    var i, card;
    for (i = 0; i < 5; i++) {
      if (i == 0) {
        card = nursery.pop();
      }else{
        card = deck.pop();
      }
      card.setAttribute("x", i * 150);
  	  card.setAttribute("y", 400);
      card.setAttributeNS("http://www.w3.org/1999/xlink","xlink:href", "https://raw.githubusercontent.com/tfabiha/unstablepics/master/" + card.getAttribute("name") + ".jpg");
      player_hand.push(card);
    }
  }

  var make_opponent_hand = function() {
    var i, card;
    for (i = 0; i < 5; i++) {
      if (i == 0) {
        card = nursery.pop();
      }else{
        card = deck.pop();
      }
      card.setAttribute("x", i * 150);
  	  card.setAttribute("y", 0);
      opponent_hand.push(card);
    }
  }

  make_player_hand();
  make_opponent_hand();

  for (i = 0; i < deck.length; i++){
  	var card = deck[i];
  	c.appendChild(card);
  }
  for (i = 0; i < nursery.length; i++){
  	var card = nursery[i];
  	c.appendChild(card);
  }
  for (i = 0; i < 5; i++){
  	var card = player_hand[i];
  	c.appendChild(card);
  	card = opponent_hand[i];
  	c.append(card);
  }
});

drawbutton.addEventListener('click', function() {
  var card = deck.pop();
  player_hand.push(card);
  if(player_hand.length > 5) {

  }
});
