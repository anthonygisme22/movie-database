import { useState } from "react";
import axios from "axios";

export default function MovieSearch() {
    const [query, setQuery] = useState("");
    const [movies, setMovies] = useState([]);

    const searchMovies = async () => {
        const res = await axios.get(`http://localhost:8000/search?query=${query}`);
        setMovies(res.data);
    };

    return (
        <div>
            <h1>Search Movies</h1>
            <input type="text" value={query} onChange={(e) => setQuery(e.target.value)} />
            <button onClick={searchMovies}>Search</button>
            <ul>
                {movies.map((movie) => (
                    <li key={movie.id}>{movie.title}</li>
                ))}
            </ul>
        </div>
    );
}