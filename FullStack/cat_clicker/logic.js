// Check for the various File API support.
if (window.File && window.FileReader && window.FileList && window.Blob) {
  // Great success! All the File APIs are supported.
} else {
  alert('The File APIs are not fully supported in this browser.');
}
function handleFileSelect(evt) {
    var files = evt.target.files; // FileList object

    // files is a FileList of File objects. List some properties.
    var output = [];
    for (var i = 0, f; f = files[i]; i++) {
      output.push('<li><strong>', escape(f.name), '</strong> (', f.type || 'n/a', ') - ',
                  f.size, ' bytes, last modified: ',
                  f.lastModifiedDate ? f.lastModifiedDate.toLocaleDateString() : 'n/a',
                  '</li>');
    }
    document.getElementById('list').innerHTML = '<ul>' + output.join('') + '</ul>';
}

document.getElementById('files').addEventListener('change', handleFileSelect, false);


// clear the screen for testing
//document.body.innerHTML = '';

var cats = ['cat.jpg','cat2.jpg','cat3.jpg','puppy1.jpg','puppy2.jpg'];

// Let's loop over the numbers in our array
for (var i = 0; i < cats.length; i++) {

    // This is the number we're on...
    var cat = cats[i];
    var catName = cat.split('.')[0];
    var count = 0;

    // We're creating a DOM element for the number
    var elem = document.createElement('div');

    var name = elem.appendChild(document.createElement('H1'));
    name.innerHTML = catName;

    //document.getElementsByTagName('H1').innerHTML = cat.split('.')[0];
    var img = elem.appendChild(document.createElement('img'));
    img.src = cat;

    var counter = elem.appendChild(document.createElement('p'));
    counter.innerHTML = count;
    

    // ... and when we click, alert the value of `num`
    elem.addEventListener('click', (function(count, counter) {
        return function() {
            count += 1;
            counter.innerHTML = count;
        };
    })(count, counter));

    document.body.appendChild(elem);
};