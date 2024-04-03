<script lang="ts">
  import Radio from '@smui/radio';
  import FormField from '@smui/form-field';
  import Button, {Label} from '@smui/button';

  export let songResults: string | string[];
  export let performedQuery: string;

  const CLIENT_ID = '';
  const SPOTIFY_CLIENT_SECRET = ''; 
  const SPOTIFY_SEARCH_ENDPOINT = 'https://api.spotify.com/v1/search';
  const SPOTIFY_OEMBED_ENDPOINT = 'https://open.spotify.com/oembed';
  const LIMIT: number = 3;
  const LIMITED_SONG_RESULTS = (songResults as string[]).slice(0, LIMIT);

  let selected: string[] = Array(LIMIT).fill('1');
  let results : string[] = [];
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

  const writeSelectedToFile = () => {
    let ratings = {
      query: performedQuery,
      results: LIMITED_SONG_RESULTS.map((item, index) => [item, selected[index]])
    }
    let fileContent = JSON.stringify(ratings);
    const element = document.createElement('a');
    const file = new Blob([fileContent], {type: 'text/json'});
    element.href = URL.createObjectURL(file);
    element.download = `${performedQuery}.txt`;
    document.body.appendChild(element); // Required for this to work in FireFox
    element.click();
  }

  LIMITED_SONG_RESULTS.forEach((song: string) => {
    search(song).then((data) => {
      getEmbedUrl(data);
    })
  });
  results = results.map((item) => {
    return item.replace(/\\/g, '');
  });
</script>

<style>
    h2 {
      font-family: 'Roboto', sans-serif;
    }
    .radio-demo {
      margin-bottom: 1rem;
    }
</style>

{#if results && results.length > 0}
<div style="width: 90%; display: flex; flex-direction: column; align-items: center;">
  <h2>Rate on a scale from 1 to 7 how relevant each result is</h2>
  {#each results as result, i}
    {@html result}
  <div class="radio-demo">
    {#each Array.from(Array(7).keys()) as option}
      <FormField>
        <Radio
          bind:group={selected[i]}
          value={option + 1}
        />
        <span slot="label">
          {option + 1}
        </span>
      </FormField>
    {/each}
  </div>  
  {/each}
  <Button on:click={() => writeSelectedToFile()}>
    <Label>Submit ratings</Label>
  </Button>
</div>
{/if} 
