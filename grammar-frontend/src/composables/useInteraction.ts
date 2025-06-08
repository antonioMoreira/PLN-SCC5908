import { inject } from "vue";
import type { Word } from "../views/TaggingView.vue";
import type { FirebaseApp } from "firebase/app";
import { ulid } from "ulid";
import {
  setDoc,
  doc,
  collection,
  getFirestore,
  type Firestore,
} from "firebase/firestore";

function publishEvent(db: Firestore, event: BaseSystemEvents) {
  const eventCollection = collection(db, "events");
  const docId = ulid(); // Use custom ID or generate one with ulid
  const docRef = doc(eventCollection, docId);
  setDoc(docRef, event);
}

export default function useInteractionEvents(id: string) {
  const firebaseApp = inject("firebase") as FirebaseApp;
  const firestore = getFirestore(firebaseApp);

  let orderingId = 0;

  function publishNewSessionEvent(serie: string, words: Word[]) {
    const event: SessionEvent = {
      sessionId: id,
      startTime: new Date(),
      serie,
      eventType: "new-session",
      words,
    };
    publishEvent(firestore, event);
  }

  function publishInteractionEvent(options: {
    targetWord: string;
    draggedTag: string;
    correctTag: string;
  }) {
    const event: InteractionEvent = {
      sessionId: id,
      orderingId: orderingId++,
      targetWord: options.targetWord,
      draggedTag: options.draggedTag,
      correctTag: options.correctTag,
      eventType: "interaction",
    };
    publishEvent(firestore, event);
  }

  return {
    publishNewSessionEvent,
    publishInteractionEvent,
  };
}

interface BaseSystemEvents {
  sessionId: string;
  eventType: "new-session" | "interaction";
}

interface SessionEvent extends BaseSystemEvents {
  startTime: Date;
  serie: string;
  eventType: "new-session";
  words: Word[];
}

interface InteractionEvent extends BaseSystemEvents {
  eventType: "interaction";
  orderingId: number;
  targetWord: string;
  draggedTag: string;
  correctTag: string;
}
