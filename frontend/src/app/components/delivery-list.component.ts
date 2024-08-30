import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { ApiService } from '../services/api.service';
import { Delivery } from '../models/delivery';
import { Observable } from 'rxjs';
import { HttpClient, HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-delivery-list',
  standalone: true,
  imports: [CommonModule, HttpClientModule],
  templateUrl: './delivery-list.component.html',
  styleUrls: ['./delivery-list.component.css']
})
export class DeliveryListComponent implements OnInit {

  data: Delivery[] = [];

  private apiUrl: string = 'http://0.0.0.0:5000/api/v1/deliveries';

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    this.processData();
  }

  getDataFromApi(): Observable<{ deliveries: Delivery[] }> {
    return this.http.get<{ deliveries: Delivery[] }>(this.apiUrl);
  }

  processData(): void {
    this.getDataFromApi().subscribe({
      next: (response) => {
        this.data = response.deliveries;
        console.log(this.data);
      },
      error: (err) => {
        console.error('Error fetching data:', err);
      },
      complete: () => {
        console.log('Fetch complete');
      }
    });
  }

  convertUTCToPST(dateStr: string): string {
    // Parse the UTC date string
    const utcDate = new Date(dateStr);
    utcDate.setDate(utcDate.getDate() + 1);
  
    // Define PST timezone options
    const options: Intl.DateTimeFormatOptions = {
      timeZone: 'America/Los_Angeles', // PST/PDT timezone
      year: 'numeric',
      month: 'long',
      day: '2-digit',
    };
  
    const pstFormatter = new Intl.DateTimeFormat('en-US', options);
    const formattedPSTDate = pstFormatter.format(utcDate);
  
    return formattedPSTDate;
  }

  
}
