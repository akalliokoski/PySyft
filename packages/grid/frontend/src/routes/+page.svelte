<script>
  import { goto } from '$app/navigation';

  async function lazyLoad() {
    if (typeof window === 'undefined') return;

    if (!window.localStorage.getItem('key')) {
      goto('/login');
    } else {
      goto('/datasets');
    }
  }
</script>

<main>
  {#await lazyLoad()}
    <title>PyGrid</title>
  {/await}
</main>
