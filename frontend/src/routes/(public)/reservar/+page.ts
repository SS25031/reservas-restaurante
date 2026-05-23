import { getPublicRestaurant } from '$lib/api/public';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ fetch }) => {
	const restaurant = await getPublicRestaurant(fetch);
	return { restaurant };
};
