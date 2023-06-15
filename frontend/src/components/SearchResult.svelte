<script lang="ts">
  export let songResults: string | string[];
  let htmlContent: string = '';
  let results : string[] = [];
  const CLIENT_ID = '6203281b0b8644bcb94fc81e4bffba2c';
  const SPOTIFY_CLIENT_SECRET = '193ccf96e0794fd9b40a6b2d15910692'; 
  const SPOTIFY_SEARCH_ENDPOINT = 'https://api.spotify.com/v1/search';
  const SPOTIFY_OEMBED_ENDPOINT = 'https://open.spotify.com/oembed';

  const getAccessToken = async () => {
    const response = await fetch('https://accounts.spotify.com/api/token', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        Authorization: `Basic ${btoa(`${CLIENT_ID}:${SPOTIFY_CLIENT_SECRET}`)}`,
      },
      body: 'grant_type=client_credentials',
    });
    const data = await response.json();
    return data.access_token;
  };

  const search = async (query: string) => {
    const accessToken = await getAccessToken();
    const response = await fetch(`${SPOTIFY_SEARCH_ENDPOINT}?q=${query}&type=track`, {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });
    const data = await response.json();
    return data.tracks.items[0].external_urls.spotify;
  };

  const getEmbedUrl = async (uri: string) => {
    const response = await fetch(`${SPOTIFY_OEMBED_ENDPOINT}?url=${uri}`, {
      method: 'GET'
    });
    const data = await response.json();
    updateResults(data.html); 
  };

  const updateResults = (item: string) => {
    results = [...results, item]
  }

  (songResults.slice(0, 3) as string[]).forEach((song: string) => {
    search(song).then((data) => {
      getEmbedUrl(data);
    })
  });
  results = results.map((item) => {
    return item.replace(/\\/g, '');
  });
  console.log(results);
</script>

{#if results && results.length > 0}
<div style="width: 90%;">
  {@html results.join('')}
</div>
{/if} 


<!-- Why is the htmlContentList not rendering? -->
