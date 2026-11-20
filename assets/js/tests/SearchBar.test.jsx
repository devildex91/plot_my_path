
import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { render, screen, fireEvent, act, cleanup } from "@testing-library/react";
import SearchBar from "../components/SearchBar.jsx";

describe("SearchBar", () => {
  beforeEach(() => {
    vi.useFakeTimers();
    vi.stubGlobal("fetch", vi.fn());
  });

  afterEach(() => {
    cleanup();
    vi.useRealTimers();
    vi.unstubAllGlobals();
    vi.restoreAllMocks();
  });

  it("renders the destination search input", () => {
    render(<SearchBar baseUrl="/destinations/0/" />);

    expect(
      screen.getByPlaceholderText("Search Destinations...")
    ).toBeInTheDocument();
  });

  it("does not search before the 300ms debounce period", async () => {
    render(<SearchBar baseUrl="/destinations/0/" />);

    fireEvent.change(screen.getByPlaceholderText("Search Destinations..."), {
      target: { value: "Paris" },
    });

    await act(async () => {
      await vi.advanceTimersByTimeAsync(299);
    });

    expect(fetch).not.toHaveBeenCalled();
  });

  it("searches after the 300ms debounce period", async () => {
    fetch.mockResolvedValue({
      json: async () => ({ results: [] }),
    });

    render(<SearchBar baseUrl="/destinations/0/" />);

    fireEvent.change(screen.getByPlaceholderText("Search Destinations..."), {
      target: { value: "Paris" },
    });

    await act(async () => {
      await vi.advanceTimersByTimeAsync(300);
    });

    expect(fetch).toHaveBeenCalledWith(
      "/destination/api/search/?q=Paris"
    );
  });

  it("encodes special characters in the search query", async () => {
    fetch.mockResolvedValue({
      json: async () => ({ results: [] }),
    });

    render(<SearchBar baseUrl="/destinations/0/" />);

    fireEvent.change(screen.getByPlaceholderText("Search Destinations..."), {
      target: { value: "New York & Paris" },
    });

    await act(async () => {
      await vi.advanceTimersByTimeAsync(300);
    });

    expect(fetch).toHaveBeenCalledWith(
      "/destination/api/search/?q=New%20York%20%26%20Paris"
    );
  });

  it("resets the debounce timer when the query changes", async () => {
    fetch.mockResolvedValue({
      json: async () => ({ results: [] }),
    });

    render(<SearchBar baseUrl="/destinations/0/" />);

    const input = screen.getByPlaceholderText("Search Destinations...");

    fireEvent.change(input, {
      target: { value: "Par" },
    });

    await act(async () => {
      await vi.advanceTimersByTimeAsync(200);
    });

    fireEvent.change(input, {
      target: { value: "Paris" },
    });

    await act(async () => {
      await vi.advanceTimersByTimeAsync(299);
    });

    expect(fetch).not.toHaveBeenCalled();

    await act(async () => {
      await vi.advanceTimersByTimeAsync(1);
    });

    expect(fetch).toHaveBeenCalledTimes(1);
    expect(fetch).toHaveBeenCalledWith(
      "/destination/api/search/?q=Paris"
    );
  });

  it("displays the loading indicator while the search request is pending", async () => {
    let resolveFetch;

    fetch.mockReturnValue(
      new Promise((resolve) => {
        resolveFetch = resolve;
      })
    );

    render(<SearchBar baseUrl="/destinations/0/" />);

    fireEvent.change(screen.getByPlaceholderText("Search Destinations..."), {
      target: { value: "Paris" },
    });

    await act(async () => {
      await vi.advanceTimersByTimeAsync(300);
    });

    expect(screen.getByText("Loading...")).toBeInTheDocument();

    await act(async () => {
      resolveFetch({
        json: async () => ({ results: [] }),
      });
    });

    expect(screen.queryByText("Loading...")).not.toBeInTheDocument();
  });

  it("displays destination results returned by the API", async () => {
    fetch.mockResolvedValue({
      json: async () => ({
        results: [
          {
            id: 1,
            name: "Eiffel Tower",
            country: "France",
            image_url: "/images/eiffel-tower.jpg",
          },
          {
            id: 2,
            name: "Louvre Museum",
            country: "France",
            image_url: "/images/louvre.jpg",
          },
        ],
      }),
    });

    render(<SearchBar baseUrl="/destinations/0/" />);

    fireEvent.change(screen.getByPlaceholderText("Search Destinations..."), {
      target: { value: "Paris" },
    });

    await act(async () => {
      await vi.advanceTimersByTimeAsync(300);
    });

    expect(screen.getByText("Eiffel Tower")).toBeInTheDocument();
    expect(screen.getByText("Louvre Museum")).toBeInTheDocument();
    expect(screen.getAllByText("France")).toHaveLength(2);
  });

  it("uses the supplied base URL when creating destination links", async () => {
    fetch.mockResolvedValue({
      json: async () => ({
        results: [
          {
            id: 1,
            name: "Eiffel Tower",
            country: "France",
            image_url: "/images/eiffel-tower.jpg",
          },
        ],
      }),
    });

    render(<SearchBar baseUrl="/destinations/0/" />);

    fireEvent.change(screen.getByPlaceholderText("Search Destinations..."), {
      target: { value: "Paris" },
    });

    await act(async () => {
      await vi.advanceTimersByTimeAsync(300);
    });

    expect(screen.getByRole("link")).toHaveAttribute(
      "href",
      "/destinations/1/"
    );
  });

  it("uses the default destination URL when no base URL is supplied", async () => {
    fetch.mockResolvedValue({
      json: async () => ({
        results: [
          {
            id: 5,
            name: "Louvre Museum",
            country: "France",
            image_url: "/images/louvre.jpg",
          },
        ],
      }),
    });

    render(<SearchBar />);

    fireEvent.change(screen.getByPlaceholderText("Search Destinations..."), {
      target: { value: "Louvre" },
    });

    await act(async () => {
      await vi.advanceTimersByTimeAsync(300);
    });

    expect(screen.getByRole("link")).toHaveAttribute(
      "href",
      "/destinations/details/5/"
    );
  });

  it("displays the destination image and its alternative text", async () => {
    fetch.mockResolvedValue({
      json: async () => ({
        results: [
          {
            id: 1,
            name: "Eiffel Tower",
            country: "France",
            image_url: "/images/eiffel-tower.jpg",
          },
        ],
      }),
    });

    render(<SearchBar baseUrl="/destinations/0/" />);

    fireEvent.change(screen.getByPlaceholderText("Search Destinations..."), {
      target: { value: "Paris" },
    });

    await act(async () => {
      await vi.advanceTimersByTimeAsync(300);
    });

    expect(screen.getByRole("img", { name: "Eiffel Tower" })).toHaveAttribute(
      "src",
      "/images/eiffel-tower.jpg"
    );
  });

  it("clears the results when the search query is emptied", async () => {
    fetch.mockResolvedValue({
      json: async () => ({
        results: [
          {
            id: 1,
            name: "Eiffel Tower",
            country: "France",
            image_url: "/images/eiffel-tower.jpg",
          },
        ],
      }),
    });

    render(<SearchBar baseUrl="/destinations/0/" />);

    const input = screen.getByPlaceholderText("Search Destinations...");

    fireEvent.change(input, {
      target: { value: "Paris" },
    });

    await act(async () => {
      await vi.advanceTimersByTimeAsync(300);
    });

    expect(screen.getByText("Eiffel Tower")).toBeInTheDocument();

    fireEvent.change(input, {
      target: { value: "" },
    });

    expect(screen.queryByText("Eiffel Tower")).not.toBeInTheDocument();
    expect(fetch).toHaveBeenCalledTimes(1);
  });
});
