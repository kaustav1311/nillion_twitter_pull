import React, { useEffect, useState } from 'react';

type Tweet = {
  date: string;
  source: string;
  author: string;
  text: string;
  link: string;
  media?: string[];
};

const TweetCard: React.FC = () => {
  const [tweets, setTweets] = useState<Tweet[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const today = new Date();
    const yyyy = today.getUTCFullYear().toString();
    const mm = (today.getUTCMonth() + 1).toString().padStart(2, '0');
    const dd = today.getUTCDate().toString().padStart(2, '0');
    const filename = `/community_feed/twitter_${yyyy}${mm}${dd}.json`;

    fetch(filename)
      .then((res) => {
        if (!res.ok) throw new Error('Could not load tweets');
        return res.json();
      })
      .then(setTweets)
      .catch((err) => setError(err.message));
  }, []);

  if (error) return <div className="text-red-500">Error loading tweets: {error}</div>;
  if (tweets.length === 0) return <div>No tweets available today.</div>;

  return (
    <div className="flex flex-col gap-4 items-center w-full">
      {tweets.map((tweet, index) => (
        <div
          key={index}
          className="w-full max-w-md p-4 border rounded-2xl shadow bg-white text-gray-800"
        >
          <div className="flex items-center gap-2 mb-2">
            <img
              src="/twitter-logo.png"
              alt="Twitter"
              className="w-8 h-8 rounded-full"
            />
            <span className="font-semibold">{tweet.author}</span>
          </div>

          <div className="whitespace-pre-line text-sm mb-2">{tweet.text}</div>

          {tweet.media && tweet.media.length > 0 && (
            <div className="flex flex-col gap-2">
              {tweet.media.map((mediaUrl, i) => (
                <img
                  key={i}
                  src={mediaUrl}
                  alt={`Tweet media ${i + 1}`}
                  className="rounded-lg w-full object-cover"
                />
              ))}
            </div>
          )}

          <div className="text-xs text-gray-500 mt-3">
            {tweet.date} ·{' '}
            <a
              href={tweet.link}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-500 hover:underline"
            >
              View on Twitter
            </a>
          </div>
        </div>
      ))}
    </div>
  );
};

export default TweetCard;

