import { useState } from "react";

const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL;

export default function MovieSearch() {
    const [query, setQuery] = useState("");
    const [movies, setMovies] = useState([]);
    const [recommendation, setRecommendation] = useState("");

    const searchMovies = async () => {
        const res = await fetch(`${backendUrl}/search?query=${query}`);
        const data = await res.json();
        setMovies(data);
    };

    const getAIRecommendation = async () => {
        const res = await fetch(`${backendUrl}/ai-recommend?description=${query}`);
        const data = await res.json();
        setRecommendation(data.recommendation);
    };

    return (
        <div className="p-4">
            <h1 className="text-2xl font-bold">Movie Database</h1>
            <input
                type="text"
                placeholder="Enter a movie name or description"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                className="border p-2 rounded-lg w-full my-2"
            />
            <div className="flex space-x-2">
                <button onClick={searchMovies} className="bg-blue-500 text-white px-4 py-2 rounded">
                    Search Movies
                </button>
                <button onClick={getAIRecommendation} className="bg-green-500 text-white px-4 py-2 rounded">
                    Get AI Recommendation
                </button>
            </div>
            <h2 className="text-xl mt-4">Results:</h2>
            <ul>
                {movies.map((movie) => (
                    <li key={movie.id}>{movie.title}</li>
                ))}
            </ul>
            {recommendation && (
                <div className="mt-4 p-2 border rounded-lg bg-gray-100">
                    <h2 className="font-bold">AI Recommendation:</h2>
                    <p>{recommendation}</p>
                </div>
            )}
        </div>
    );
}
