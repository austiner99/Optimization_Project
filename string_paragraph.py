'''
This is the test string
'''
# Import necessary libraries
import numpy as np


string = " \
The sun’s warm glow fell across the field. A breeze stirred, rustling leaves as birds chirped. The dog’s bark echoed while a cat lounged nearby. People walked along quiet paths, sharing thoughts. What joy exists in moments like these? Clouds drifted above, shadows shifting below. Foxes dashed through the brush. Time’s passage often feels swift. Yet, laughter lingers. Jars of jam lined the shelf. Vivid quilts hung, displaying vibrant hues. Zebras grazed in far-off lands. Quirky scenes unfold daily. Few question why. Life’s charm, both simple and profound, remains constant. Is there anything more precious than this? \" \
Children played along the park’s edge, their laughter mingling with the breeze. Ducks glided across the pond, ripples trailing behind. Tall trees stood in silent watch, their branches swaying softly. Nearby, a gardener tended flowers, carefully pruning each stem. The air smelled of fresh earth and blooming petals. Squirrels scampered up tree trunks, their tails flicking in delight. Nature thrived, unburdened by time’s relentless march. \
A man with a weathered hat sat upon a bench, his hands clasped together. His eyes traced the flight of a passing bird. What memories lingered within his thoughts? Each wrinkle on his face told a story, shaped by years of joy and sorrow. A nearby jogger passed, earbuds in, oblivious to the world around her. Life continued, ever in motion. \
By the water’s edge, a family spread a picnic blanket. Sandwiches, fruit, and lemonade filled their basket. The youngest child giggled as she chased a butterfly. The parents watched with gentle smiles, savoring the fleeting moments of innocence. Sunlight dappled the ground, illuminating patches of vibrant green. A dragonfly hovered above the reeds, its wings glinting. \
In the distance, an old farmhouse stood, its red paint peeling. Wooden shutters, once bright, now bore the marks of age. The wind stirred the tall grass, sending waves across the golden field. A black cat perched on the porch, eyes gleaming. Beside the barn, rusted tools lay abandoned. Yet, even in neglect, beauty endured. \
A narrow dirt road wound through the countryside. Along its path, wildflowers bloomed in bursts of yellow and purple. Cows grazed lazily, tails flicking away flies. A lone cyclist pedaled past, the hum of tires blending with the chirp of crickets. Overhead, a hawk soared, scanning the ground below. \
Night approached, and the sky deepened to indigo. Stars blinked into existence, scattered like gems. A crescent moon hung low, casting silver light. In a small town nearby, streetlamps flickered on. Porch lights glowed warmly, welcoming home weary travelers. Laughter spilled from an open window, the sound of a family gathered for dinner. \
A couple strolled hand in hand, their steps in perfect rhythm. They paused beneath a lamppost, its glow casting a halo around them. The man whispered something, drawing a soft laugh from his companion. Shadows danced along the pavement. Above them, the stars watched in silent approval. \
Time passed, as it always does. Seasons changed, painting the world in hues of gold, crimson, and green. Children grew, their laughter echoing through the years. Leaves fell, carpeting the ground in a crunchy mosaic. Snow blanketed rooftops, muffling the world in a quiet embrace. Yet, the cycle continued. \
In spring, blossoms burst forth, coloring branches with pink and white. Bees buzzed, drawn to the sweet nectar. Farmers tilled the soil, their hands darkened with earth. Rain fell in gentle showers, nourishing the eager roots. Frogs croaked from hidden ponds. Life thrived. \
Summer brought long days of warmth. Fields of wheat swayed under the sun’s golden gaze. Children dashed through sprinklers, squealing with delight. Ice cream dripped from cones, melting faster than it could be licked. Fireflies blinked in the twilight, their glow like tiny stars. Laughter echoed from backyard gatherings. \
Autumn arrived with a crisp breeze. Leaves turned brilliant shades of amber and scarlet. Pumpkins dotted fields, their orange shells gleaming. Families wandered through corn mazes, laughter guiding their way. Bonfires crackled, sending sparks skyward. The scent of cinnamon and apple cider lingered in the air. \
Winter followed, wrapping the world in icy stillness. Frost traced delicate patterns upon windowpanes. Children built snowmen, their mittens damp with melted snow. Smoke curled from chimneys, mingling with the cold air. The ground glittered beneath the moonlight, each snowflake unique. Silence reigned, broken only by the crunch of boots upon snow. \
Yet, through every season, life endured. The fox still leaped, the dog barked, and the cat purred. People gathered, shared stories, and held one another close. Time moved forward, but memories remained. And in those memories, joy blossomed. \
A robin sang at dawn, its cheerful notes welcoming the sun. Dew clung to blades of grass, shimmering like jewels. A farmer’s rooster crowed, greeting the day with pride. Somewhere, a child stirred beneath warm blankets, dreaming of distant adventures. \
The ocean’s waves crashed against the shore, sending salty mist into the air. Gulls circled above, their cries mingling with the breeze. A lighthouse stood tall, its beam sweeping across the darkened waters. Sailboats bobbed in the harbor, their sails furled. \
Farther inland, mountains rose, their peaks kissed by clouds. Pine trees lined the slopes, their needles dusted with snow. Hikers paused to admire the view, their breath visible in the thin air. A hawk soared, its sharp eyes scanning the forest below. \
In bustling cities, people hurried along crowded sidewalks. Taxi horns blared, and street vendors called to passing customers. Neon signs flickered, illuminating the night. Yet, even amidst the chaos, beauty lingered. Musicians played on street corners, their melodies weaving through the urban hum. \
In quieter towns, church bells rang, their chimes echoing across the valley. Children rode bicycles along winding paths. Farmers tended their fields, the scent of fresh hay filling the air. Life moved at a gentler pace. \
As twilight fell, the sky blazed with hues of pink and orange. Couples sat on porches, watching the day’s end. Fireflies emerged, their soft glow dancing in the dark. Stars appeared, each one a reminder of the vastness beyond. \
The world whispered its stories to those who listened. From the rustle of leaves to the crash of waves, every sound held meaning. Even the silence spoke, offering solace to those who sought it. \
So, as time marches on, may we pause to savor the moments that remain. The laughter of loved ones, the warmth of the sun, the simple joy of a breeze through the trees. For in these fleeting instants, life’s beauty endures. \
And perhaps, that is enough. \
"


def string_to_index_optimized(string):
    # Vectorized approach for string-to-index conversion
    string = string.lower().replace(" ", "")
    char_map = {chr(i + 97): i for i in range(26)}
    char_map.update({'.': 26, ',': 27, '?': 28, "'": 29})
    return np.array([char_map.get(char, -1) for char in string])

string_index = string_to_index_optimized(string)
