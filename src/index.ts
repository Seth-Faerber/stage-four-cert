import express from "express";
import dotenv from "dotenv";
import { authMiddleware } from "./auth";
import usersRouter from "./app/api/users/route";
import healthRouter from "./app/api/health/route";

dotenv.config();

const app = express();
app.use(express.json());
app.use(authMiddleware);

app.use("/api/health", healthRouter);
app.use("/api/users", usersRouter);

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});

export default app;
