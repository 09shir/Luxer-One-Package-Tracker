import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { DeliveryListComponent } from './components/delivery-list.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, DeliveryListComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'package-tracker-frontend';
}
