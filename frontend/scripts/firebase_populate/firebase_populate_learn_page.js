import { addDoc, collection } from 'firebase/firestore';

import { firestore } from '../firebase.js';

const biases = [
  {
    name: 'Confirmation Bias',
    description:
      "The tendency to search for, interpret, favor, and recall information in a way that confirms one's preexisting beliefs or theories.",
    example:
      'A person who believes in astrology might only remember the instances when horoscopes seemed accurate and ignore the times they were wrong.',
    impact:
      'It can lead to a skewed perception of reality, reinforcing incorrect beliefs and making it difficult to consider alternative viewpoints.',
  },
  {
    name: 'Anchoring Bias',
    description:
      "The tendency to rely too heavily on the first piece of information encountered (the 'anchor') when making decisions.",
    example:
      'If a person sees a T-shirt priced at $1,000 and then sees another one for $100, they may perceive the second T-shirt as cheap.',
    impact:
      'It can affect negotiations, pricing strategies, and decision-making processes by unduly influencing judgments.',
  },
  {
    name: 'Halo Effect',
    description:
      'The tendency for an impression created in one area to influence opinion in another area.',
    example: 'If someone is attractive, people may also assume they are intelligent and kind.',
    impact:
      'It can lead to biased assessments of individuals, particularly in hiring, promotions, and performance evaluations.',
  },
  {
    name: 'Framing Effect',
    description:
      'The tendency to react to a particular choice based on how it is presented, e.g., as a loss or as a gain.',
    example:
      'People are more likely to choose a surgery with a 90% survival rate than one with a 10% mortality rate, even though they are the same.',
    impact:
      'It can influence decisions in marketing, policy-making, and everyday choices by altering perceptions.',
  },
  {
    name: 'Negativity Bias',
    description:
      'The tendency to give more weight to negative information than positive information.',
    example: 'People tend to remember criticisms more than compliments.',
    impact:
      'It can lead to an overly pessimistic view of situations, affecting mental health and decision-making.',
  },
  {
    name: 'Availability Heuristic',
    description:
      'The tendency to overestimate the likelihood of events based on their availability in memory, which is often influenced by recent or vivid events.',
    example:
      'After seeing news reports about airplane crashes, people might think air travel is more dangerous than it is.',
    impact: 'It can distort risk assessments and lead to irrational fears or overreactions.',
  },
  {
    name: 'Selection Bias',
    description:
      'The bias introduced by the selection of individuals, groups, or data for analysis in such a way that proper randomization is not achieved.',
    example:
      'Surveying only those who visit a particular website might not represent the general population.',
    impact:
      'It can lead to inaccurate conclusions and undermine the validity of research findings.',
  },
  {
    name: 'Survivorship Bias',
    description:
      "The logical error of concentrating on the people or things that 'survived' some process and overlooking those that did not because of their lack of visibility.",
    example:
      'Studying successful companies without considering failed ones can lead to incorrect conclusions about business success.',
    impact:
      'It can create a false sense of understanding and success, leading to misguided decisions.',
  },
  {
    name: 'Bandwagon Effect',
    description: 'The tendency to adopt beliefs and ideas because many others do.',
    example:
      'People might start believing in a fad diet because it is popular, not because it is scientifically sound.',
    impact: 'It can lead to conformity and suppress individual critical thinking.',
  },
  {
    name: 'Overconfidence Bias',
    description:
      "The tendency to be more confident in one's own abilities, such as driving, teaching, or spelling, than is objectively warranted.",
    example:
      'A person might believe they can complete a project in a week when it realistically takes a month.',
    impact: 'It can result in underestimating risks, overcommitting, and poor decision-making.',
  },
];
const toneAnalysis = [
  {
    name: "Plutchik's Model",
    description:
      'A model of emotions based around concentric circles with the center representing core emotions and the outer circles representing more intense emotions. The outer circles are also formed through combination of the emotions in the inner circle.',
    example:
      'Some examples of combinations are envy which is a combination of sadness and anger, or despair, which is a combination of fear and sadness.',
    impact:
      'Understanding emotions on a scale of intensity as well as knowing the combinations that make up more complex ones can make it easier to discern which base emotions a piece of writing is appealing to.',
  },
  {
    name: 'Joy',
    description:
      'The positive emotion associated with contentment, pleasure, and excitement. Sometimes joy may be flagged by an LLM when a page returns a highly positive sentiment, or when the text includes descriptions of achievements, celebrations, or emotional states such as satisfaction.',
    example:
      'Articles that are more likely to score more prominently in joy are press releases, event announcements, or advertisements.',
    impact:
      'Since joy and happiness are a goal for most people, an article that scores prominently in joy or has many entities or keywords meant to evoke joy may be trying to steer it’s audience a certain way.',
  },
  {
    name: 'Sadness',
    description:
      'Sadness is characterized by feelings of grief and can sometimes be flagged by an LLM when a page returns a particularly low sentiment score. Other indicators of sadness in a text include descriptions or references to concepts such as loneliness, disappointment, or personal tragedy.',
    example:
      'Sadness is more likely to be found linked to specific entities or attributes in a text rather than the title or document as a whole. This can be particularly prominent in current event news articles.',
    impact:
      'Sadness on its own isn’t a particularly strong indicator of attempts of manipulation, but is still an important factor when contextually analyzing a piece of writing. Try asking yourself if the presence of an entity or concept that evokes sadness is tied to any other specific concept and why it would be used in that way.',
  },
  {
    name: 'Fear',
    description:
      'An emotion characterized by feelings of concern or apprehension and set off by the perception of a threat.',
    example:
      'An article aimed at a specific political base will often return a score of fear when discussing the opposition.',
    impact:
      'Like disgust, the fear score returned when using an LLM is a more subtle version of the emotion. Often the perceived threat is implicit, and may be aimed at a particular group and invisible to others. Identifying when fear is being used and how can be important not only in combating disinformation, but also to understanding those with differing beliefs.',
  },
  {
    name: 'Anger',
    description:
      'In textual analysis anger is detected through words signaling irritation or frustration, and may indicate a perceived injustice, or strong opposition towards a concept.',
    example:
      'Many titles will return a high score of anger, which is a conscious decision on the part of many websites and news organizations.',
    impact:
      'Anger is an important part of a phenomenon called emotional contagion, where seeing others express a strong emotion can lead a person to engaging similarly in the conversation. Its important to be aware of this online, as websites and organizations may look to capitalize on this to drive engagement on their platforms.',
  },
  {
    name: 'Disgust',
    description:
      'In contrast to how we may normally think of disgust, here it refers more generically to an expression of aversion, or disdain.',
    example:
      'Articles referencing money will often return disgust. Part of this could be due to negative associations such as corruption or inequality, while another part could be an aversion to talking about money or material wealth in certain cultures.',
    impact:
      'Disgust is a valuable tool for seeking out manipulation, as it is can be used as a justification for smuggling in other assertions for an an undesirable entity or concept. In Plutchik’s model it is the opposite of trust, which is why VeritasAI uses an absence of disgust as a possible indicator for trust.',
  },
];

async function populateBiases() {
  const biasesCollection = collection(firestore, 'biases');
  for (const bias of biases) {
    await addDoc(biasesCollection, bias);
    for (const tone of toneAnalysis) {
      await addDoc(biasesCollection, tone);
    }
  }
  console.log('Biases have been added to Firebase');
}

populateBiases();
