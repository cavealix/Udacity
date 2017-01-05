var initialCats = [
    {
        clickCount: 0,
        name: 'Tabby',
        imgSrc: 'img/22252709_010df3379e_z.jpg',
        nicknames: ['thiscat', 'thatcat']
    },
    {
        clickCount: 0,
        name: 'Corban',
        imgSrc: 'img/434164568_fea0ad4013_z.jpg',
        nicknames: ['thiscat', 'thatcat']
    },
    {
        clickCount: 0,
        name: 'Wayne',
        imgSrc: 'img/1413379559_412a540d29_z.jpg',
        nicknames: ['thiscat', 'thatcat']
    },
    {
        clickCount: 0,
        name: 'Tigger',
        imgSrc: 'img/4154543904_6e2428c421_z.jpg',
        nicknames: ['thiscat', 'thatcat']
    }
];

var Cat = function(data) {
    this.clickCount = ko.observable(data.clickCount);
    this.name = ko.observable(data.name);
    this.imgSrc = ko.observable(data.imgSrc);

    this.level = ko.computed(function() {
        if (this.clickCount() < 2) {
            return 'Newborn';
        }
        else if (this.clickCount() < 5) {
            return 'Infant';
        }
        else {
            return 'toddler';
        }
    }, this);

    this.nicknames = ko.observableArray(data.nicknames);
}

var ViewModel = function() {
    var self = this;

    this.catList = ko.observableArray([]);
    this.nameList = ko.observableArray([]);

    //build array of cats
    initialCats.forEach( function(catItem){
        self.catList.push( new Cat(catItem) );
        self.nameList.push( catItem.name );
    });

    this.currentCat = ko.observable( this.catList()[0] );

    this.switchCat = function(cat) {
        self.currentCat(cat);
    };

    this.incrementCounter = function() {
        this.clickCount(this.clickCount() + 1);
    };

}

ko.applyBindings(new ViewModel());