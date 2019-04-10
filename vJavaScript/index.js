const theMovieDbKey = "api_key=febbb1e930c6b293e94f9d2b77aa47cc";
const theMovieDbRestUrl = "https://api.themoviedb.org/3";
const theImdbUrl = "https://www.imdb.com/title/";
const theDuckDuckGoUrl = "https://duckduckgo.com/?q=";
const theGoogleUrl = "https://www.google.com/search?q=critica+"

var movieReady = new Event("movieReady");

function buildList() {
    document.getElementById("outputBox").value = "";    
    document.getElementById("movieCount").innerHTML = "";
    document.getElementById("movies").innerHTML = "";

    let movieList = document.getElementById("inputBox").value;
    const fullRegex = /(Dia\W\d\d\W[-–]\W(.+),.+)\n+(\(((.+),\W)?.+,\W(\d{4}),.+\))/gm;
    let m;
    let i = 0;

    while ((m = fullRegex.exec(movieList)) !== null) {
        // This is necessary to avoid infinite loops with zero-width matches
        if (m.index === fullRegex.lastIndex) {
            fullRegex.lastIndex++;
        }                

        let movie = {
            headerT: m[1],
            headerB: m[3],
            titlePt: m[2],
            titleOr: m[5] === undefined? m[2] : m[5],
            year: m[6]
        };

        setTimeout(function(){getMovie(movie);}, 1500);                                
        i++;
        document.getElementById("movieCount").innerHTML = i + " filmes em lista!";
    }  
}

function getMovie(movie) {
    let title = movie.titleOr;
    let year = movie.year;

    console.log("Searching for " + title + ", " + year + "...");

    // Creating the query:     
    let query = theMovieDbRestUrl + "/search/movie?year=" + year + "&include_adult=false&page=1&query=" + title + "&" + theMovieDbKey;

    // Creating the request:
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            let result = JSON.parse(this.responseText).results[0];

            try {
                movie.id = result.id;                
                getImdbId(movie);
                populateMovieWithCrew(movie);

            } catch (exception) {
                console.log("Failed to find " + title);
            }
        }
    };

    xhttp.open("GET", query, true);
    xhttp.send();
}

function getImdbId(movie) {
    let query = theMovieDbRestUrl + "/movie/" + movie.id + "?" + theMovieDbKey;

    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            let result = JSON.parse(this.responseText);
            movie.imdb = result.imdb_id;
        }
    };
    xhttp.open("GET", query, true);
    xhttp.send();
}

function getSinopse() {
    let query = "https://cinecartaz.publico.pt/Filme/390393_diamantino";

    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            let result = JSON.parse(this.responseText);
            console.log(result);
        }
    };
    xhttp.open("GET", query, true);
    xhttp.send();
}

function populateMovieWithCrew(movie) {
    let query = theMovieDbRestUrl + "/movie/" + movie.id + "/credits" + "?" + theMovieDbKey;

    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            let result = JSON.parse(this.responseText);

            // The arrow sintax is ES6 only
            movie.director = result.crew.filter(person => person.job == "Director")[0].name;
            movie.writers = result.crew.filter(person => person.department == "Writing").map(person => person.name + " (" + person.job + ")");
            movie.cast = result.cast.slice(0, 5).map(person => person.name);
            movie.music = result.crew.filter(person => person.job.indexOf("Music") !== -1).map(person => person.name + " (" + person.job + ")");
            movie.editing = result.crew.filter(person => person.job == "Editor").map(person => person.name + " (" + person.job + ")");
            movie.cinematography = result.crew.filter(person => person.job == "Director of Photography").map(person => person.name + " (" + person.job + ")");

            // console.log(movie);

            printMovie(movie);
        }
    };
    xhttp.open("GET", query, true);
    xhttp.send();
}

function printMovie(movie) {
    console.log(movie);
    let template = `<p>
        ${movie.headerT}<br />
        ${movie.headerB}<br />
        
        <a href="${theImdbUrl + movie.imdb}/fullcredits/" target="_blank">[IMDB]</a>             
        <a href="${theDuckDuckGoUrl}cinecartaz+${movie.titlePt.split(" ").join("+")}+${movie.year}" target="_blank">[CINECARTAZ]</a>        
        <a href="http://www.apaladewalsh.com/?s=${movie.titleOr.split(" ").join("+")}+${movie.director.split(" ").join("+")}" target="_blank">[PALA DE WALSH]</a> 
        <a href="http://www.rtp.pt/cinemax/?headline=20&visual=7&search=${movie.titlePt.split(" ").join("+")}+${movie.director.split(" ").join("+")}&criticas_page=1#criticas" target="_blank">[CINEMAX]</a> 
        <a href="http://www.magazine-hd.com/apps/wp/?s=${movie.titlePt.split(" ").join("+")}+${movie.director.split(" ").join("+")}" target="_blank">[MAGAZINE HD]</a> 
        <a href="http://www.c7nema.net/component/search/?searchword=${movie.titlePt.split(" ").join("+")}+${movie.director.split(" ").join("+")}" target="_blank">[C7NEMA]</a> 
        <a href="${theGoogleUrl}${movie.titlePt.split(" ").join("+")}+${movie.year}" target="_blank">[GOOGLE]</a>
        </p>`;
        let templatePlain = `
${movie.headerT}
${movie.headerB}

Interpretação: ${movie.cast.join(", ")}
Argumento: ${movie.writers.join(", ")}
Música: ${movie.music.join(", ")}
Cinematografia: ${movie.cinematography.join(", ")}
Edição: ${movie.editing.join(", ")}

Sinopse: 

Crítica: 

//////////////////////////////////////////////////////////////

`;

    document.getElementById("movies").innerHTML += template;
    document.getElementById("outputBox").value += templatePlain;
}