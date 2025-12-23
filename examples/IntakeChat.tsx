import { useState } from "react";

type Role = "assistant" | "user";

interface ChatMessage {
  role: Role;
  content: string;
}

export interface LearningProfilePayload {
  name: string;
  learning_goals: string[];
  learning_topics: string[];
  current_level: {
    overall: "Beginner" | "Intermediate" | "Advanced" | "Mixed";
    notes?: string;
  };
  preferred_providers: string[];
  special_requirements: string[];
  time_commitment: {
    hours_per_week: number;
    timeframe_weeks: number | null;
  };
}

export default function IntakeChat({
  onComplete,
}: {
  onComplete: (profile: LearningProfilePayload) => void;
}) {
  const [step, setStep] = useState(0);
  const [input, setInput] = useState("");
  const [chat, setChat] = useState<ChatMessage[]>([
    { role: "assistant", content: "Before we start, what should I call you?" },
  ]);

  const [profile, setProfile] = useState<LearningProfilePayload>({
    name: "",
    learning_goals: [],
    learning_topics: [],
    current_level: { overall: "Beginner" },
    preferred_providers: [],
    special_requirements: [],
    time_commitment: { hours_per_week: 6, timeframe_weeks: null },
  });

  function pushUser(msg: string) {
    setChat((c) => [...c, { role: "user", content: msg }]);
  }

  function pushAssistant(msg: string) {
    setChat((c) => [...c, { role: "assistant", content: msg }]);
  }

  function next() {
    setInput("");
    setStep((s) => s + 1);
  }

  function submitText() {
    if (!input.trim()) return;
    pushUser(input);

    switch (step) {
      case 0:
        setProfile((p) => ({ ...p, name: input }));
        pushAssistant("What are you learning for right now? You can mention more than one goal.");
        break;

      case 1:
        setProfile((p) => ({
          ...p,
          learning_goals: input.split(",").map((s) => s.trim()),
        }));
        pushAssistant("What topics do you want to focus on? You can list multiple areas.");
        break;

      case 2:
        setProfile((p) => ({
          ...p,
          learning_topics: input.split(",").map((s) => s.trim()),
        }));
        pushAssistant("How would you describe your current level overall?");
        break;

      case 4:
        setProfile((p) => ({
          ...p,
          special_requirements: input ? input.split(",").map((s) => s.trim()) : [],
        }));
        pushAssistant("How many hours per week can you realistically commit?");
        break;

      default:
        break;
    }

    next();
  }

  function chooseLevel(level: LearningProfilePayload["current_level"]["overall"]) {
    pushUser(level);
    setProfile((p) => ({
      ...p,
      current_level: { overall: level },
    }));
    pushAssistant("Do you have preferred course providers? (You can choose multiple.)");
    next();
  }

  function toggleProvider(pv: string) {
    setProfile((p) => ({
      ...p,
      preferred_providers: p.preferred_providers.includes(pv)
        ? p.preferred_providers.filter((x) => x !== pv)
        : [...p.preferred_providers, pv],
    }));
  }

  function confirmProviders() {
    pushUser(profile.preferred_providers.join(", ") || "No preference");
    pushAssistant("Any special requirements? (certifications, language, tools, etc.)");
    next();
  }

  function chooseHours(h: number) {
    pushUser(`${h} hours / week`);
    setProfile((p) => ({
      ...p,
      time_commitment: { ...p.time_commitment, hours_per_week: h },
    }));
    pushAssistant("Do you have a target timeframe?");
    next();
  }

  function chooseTimeframe(w: number | null) {
    pushUser(w ? `${w} weeks` : "No deadline");
    setProfile((p) => ({
      ...p,
      time_commitment: { ...p.time_commitment, timeframe_weeks: w },
    }));
    pushAssistant("Here’s what I’ve understood. Ready to generate your plan?");
    next();
  }

  function finish() {
    onComplete(profile);
  }

  return (
    <div className="intake">
      <div className="chat">
        {chat.map((m, i) => (
          <div key={i} className={`msg ${m.role}`}>
            {m.content}
          </div>
        ))}
      </div>

      {step === 3 && (
        <div className="choices">
          {["Beginner", "Intermediate", "Advanced", "Mixed"].map((l) => (
            <button key={l} onClick={() => chooseLevel(l as any)}>
              {l}
            </button>
          ))}
        </div>
      )}

      {step === 5 && (
        <div className="choices">
          {["Coursera", "edX", "Udemy", "YouTube", "Kaggle Learn", "No preference"].map((pv) => (
            <button key={pv} onClick={() => toggleProvider(pv)}>
              {pv}
            </button>
          ))}
          <button onClick={confirmProviders}>Continue</button>
        </div>
      )}

      {step === 6 && (
        <div className="choices">
          {[4, 6, 10].map((h) => (
            <button key={h} onClick={() => chooseHours(h)}>
              {h} hrs/week
            </button>
          ))}
        </div>
      )}

      {step === 7 && (
        <div className="choices">
          {[4, 8, 12].map((w) => (
            <button key={w} onClick={() => chooseTimeframe(w)}>
              {w} weeks
            </button>
          ))}
          <button onClick={() => chooseTimeframe(null)}>No deadline</button>
        </div>
      )}

      {(step < 3 || step === 4) && (
        <div className="input">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your answer…"
            onKeyDown={(e) => e.key === "Enter" && submitText()}
          />
          <button onClick={submitText}>Send</button>
        </div>
      )}

      {step === 8 && (
        <button className="primary" onClick={finish}>
          Generate My Plan
        </button>
      )}
    </div>
  );
}
